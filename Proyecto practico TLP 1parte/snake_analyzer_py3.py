
# Analizador para archivos .brik:
# - Lexer: separa el texto en tokens (palabras, números, símbolos)
# - Parser: arma un (AST) con clave = valor, objetos { } y listas [ ]
# - Validación mínima: chequeos básicos para no aceptar config absurda
# - Guardado: escribe un archivo de texto "arbol_snake.ast"

import re
import os
import sys
import json  # para imprimir el AST como vista previa en consola 

# =========================
# 1) LEXER (tokenizador)
# =========================
class Tokenizer():
    """
    Convierte texto .brik en tokens.
    Tipos de token que sacamos:
      - STRING: "texto"
      - NUMBER: 12, -3, 4.5
      - OPERATOR: { } [ ] = , ;
      - IDENTIFIER: nombres tipo velocidad_inicial, regla_obstaculos, etc.
      - BOOL: si/no -> True/False
    """
    def __init__(self, source_code):
        self.source = source_code
        self.tokens = []

        # 1: "cadena"
        # 2: número (entero o decimal, con signo)
        # 3: operadores { } [ ] = , ;
        # 4: identificadores (letras/números/_/-)
        self._token_re = re.compile(
            r'"([^"]*)"|(-?\d+\.\d+|-?\d+)|(\{|\}|\[|\]|=|,|;)|([A-Za-z_][A-Za-z0-9_-]*)'
        )

    def tokenize(self):
        lines = self.source.splitlines()
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                # Línea vacía o comentario
                continue

            # Partimos la línea en tokens usando el regex
            for g in self._token_re.findall(line):
                s, num, op, ident = g

                if s:  # "texto"
                    self.tokens.append(('STRING', s))
                elif num:  # número
                    self.tokens.append(('NUMBER', float(num) if '.' in num else int(num)))
                elif op:  # operador suelto
                    self.tokens.append(('OPERATOR', op))
                elif ident:  # identificador o booleano si/no
                    if ident == 'si':
                        self.tokens.append(('BOOL', True))
                    elif ident == 'no':
                        self.tokens.append(('BOOL', False))
                    else:
                        self.tokens.append(('IDENTIFIER', ident))

        return self.tokens


# =========================
# 2) PARSER
# =========================
class Parser():
    """
    Construye un AST con reglas simples:
      - Asignaciones top-level:  clave = valor
      - valor puede ser: STRING / NUMBER / BOOL / objeto { ... } / lista [ ... ]
      - En listas, si aparece un IDENTIFIER, se toma como referencia
        a algo top-level ya definido (por nombre).
    """
    def __init__(self, tokens):
        self.tokens = tokens
        self.i = 0
        self.symbol_table = {}  # aquí queda el AST raíz

    def parse(self):
        while self.i < len(self.tokens):
            if self.peek() is None:
                break

            key = self.get()
            if key[0] != 'IDENTIFIER':
                raise SyntaxError("Se esperaba un identificador, se encontró %s" % (key[1],))

            eq = self.get()
            if eq is None or not (eq[0] == 'OPERATOR' and eq[1] == '='):
                raise SyntaxError("Se esperaba '=', se encontró %s" % (eq[1] if eq else 'EOF',))

            value = self.parse_value()

            if key[1] in self.symbol_table:
                raise SyntaxError("Clave duplicada '%s'" % key[1])

            self.symbol_table[key[1]] = value

            # Permitimos ';' al final (opcional)
            if self.peek() and self.peek()[0] == 'OPERATOR' and self.peek()[1] == ';':
                self.get()

        return self.symbol_table

    # Helpers de lectura
    def get(self):
        if self.i < len(self.tokens):
            t = self.tokens[self.i]
            self.i += 1
            return t
        return None

    def peek(self):
        if self.i < len(self.tokens):
            return self.tokens[self.i]
        return None

    # Lectura de valores
    def parse_value(self):
        t = self.peek()
        if t is None:
            raise SyntaxError("Se esperaba un valor después de '='")

        tt, tv = t

        if tt in ('STRING', 'NUMBER', 'BOOL'):
            self.i += 1
            return tv

        if tt == 'OPERATOR' and tv == '{':
            return self.parse_block()

        if tt == 'OPERATOR' and tv == '[':
            return self.parse_list()

        if tt == 'IDENTIFIER':
            # referencia a algo top-level ya definido
            self.i += 1
            if tv not in self.symbol_table:
                raise NameError("El identificador '%s' no ha sido definido." % tv)
            return self.symbol_table[tv]

        raise SyntaxError("Valor inesperado '%s'" % tv)

    def parse_block(self):
        self.get()  # consume '{'
        d = {}

        while self.peek() and not (self.peek()[0] == 'OPERATOR' and self.peek()[1] == '}'):
            k = self.get()
            if k[0] != 'IDENTIFIER':
                raise SyntaxError("En objeto: se esperaba identificador, llegó %s" % k[1])

            eq = self.get()
            if eq is None or not (eq[0] == 'OPERATOR' and eq[1] == '='):
                raise SyntaxError("En objeto: se esperaba '=', llegó %s" % (eq[1] if eq else 'EOF',))

            v = self.parse_value()

            if k[1] in d:
                raise SyntaxError("En objeto: clave duplicada '%s'" % k[1])

            d[k[1]] = v

            # Permitimos coma o ; como separadores
            if self.peek() and self.peek()[0] == 'OPERATOR' and self.peek()[1] in (',', ';'):
                self.get()

        rb = self.get()
        if rb is None or not (rb[0] == 'OPERATOR' and rb[1] == '}'):
            raise SyntaxError("Falta '}' de cierre")
        return d

    def parse_list(self):
        self.get()  # consume '['
        a = []

        while self.peek() and not (self.peek()[0] == 'OPERATOR' and self.peek()[1] == ']'):
            # Si vemos IDENTIFIER, lo tratamos como referencia a top-level
            if self.peek()[0] == 'IDENTIFIER':
                name = self.get()[1]
                if name not in self.symbol_table:
                    raise NameError("El identificador '%s' no ha sido definido." % name)
                a.append(self.symbol_table[name])
            else:
                a.append(self.parse_value())

            if self.peek() and self.peek()[0] == 'OPERATOR' and self.peek()[1] == ',':
                self.get()

        rb = self.get()
        if rb is None or not (rb[0] == 'OPERATOR' and rb[1] == ']'):
            raise SyntaxError("Falta ']' de cierre")
        return a


# =========================
# 3) VALIDACIÓN MÍNIMA
# =========================
def _es_int(x):   return isinstance(x, int) and not isinstance(x, bool)
def _es_num(x):   return isinstance(x, (int, float)) and not isinstance(x, bool)
def _es_vec2(v):  return isinstance(v, list) and len(v) == 2 and all(_es_int(c) for c in v)

def validate_min(ast):
    """
    Solo revisamos lo básico:
      - dimensiones_tablero: [ancho, alto] con enteros > 0
      - velocidad_inicial: número > 0
      - serpiente_basica: dirección unitaria y spawn dentro del tablero (si está)
    """
    errores = []

    dims = ast.get('dimensiones_tablero')
    if not (isinstance(dims, list) and len(dims) == 2 and all(_es_int(n) and n > 0 for n in (dims or []))):
        errores.append("dimensiones_tablero debe ser [ancho:int>0, alto:int>0]")

    v0 = ast.get('velocidad_inicial')
    if not (_es_num(v0) and v0 > 0):
        errores.append("velocidad_inicial debe ser número > 0")

    sb = ast.get('serpiente_basica')
    if isinstance(sb, dict):
        if 'direccion_inicial' in sb:
            v = sb['direccion_inicial']
            if not (_es_vec2(v) and abs(v[0]) + abs(v[1]) == 1):
                errores.append("serpiente_basica.direccion_inicial debe ser [dx,dy] unitario")
        if 'spawn_inicial' in sb and isinstance(dims, list):
            sp = sb['spawn_inicial']
            if not _es_vec2(sp):
                errores.append("serpiente_basica.spawn_inicial debe ser [x,y]")
            else:
                x, y = sp; w, h = dims
                if not (0 <= x < w and 0 <= y < h):
                    errores.append("serpiente_basica.spawn_inicial fuera del tablero")
    elif sb is not None and not isinstance(sb, dict):
        errores.append("serpiente_basica debe ser objeto")

    return errores


# =========================
# 4) PRETTY PRINTER .ast
# =========================
def _fmt_bool(b): return 'si' if b else 'no'

def pretty_ast(v, indent=0):
    sp = ' ' * indent
    if isinstance(v, dict):
        s = '{\n'
        for k in sorted(v.keys()):
            s += f"{sp}  {k} = {pretty_ast(v[k], indent+2)}\n"
        s += sp + '}'
        return s
    if isinstance(v, list):
        # Si la lista tiene objetos/listas, la hacemos multilínea
        if any(isinstance(x, (dict, list)) for x in v):
            s = '[\n'
            for idx, el in enumerate(v):
                s += sp + '  ' + pretty_ast(el, indent+2)
                if idx != len(v)-1: s += ','
                s += '\n'
            s += sp + ']'
            return s
        else:
            return '[' + ', '.join(pretty_ast(x, 0) for x in v) + ']'
    if isinstance(v, str):
        return '"' + v.replace('\\','\\\\').replace('"','\\"') + '"'
    if isinstance(v, bool):
        return _fmt_bool(v)
    return str(v)


# =========================
# 5) ZONA DE EJECUCIÓN
# =========================
if __name__ == '__main__':
    # 1) Archivo de entrada
    file_path = "Snake.brik" 
    ast_out   = "arbol_snake.ast"

    # 2) Cargar el archivo .brik
    if not os.path.exists(file_path):
        print("Error: El archivo '%s' no se encontró." % file_path)
        sys.exit(1)
    with open(file_path, 'r', encoding='utf-8') as f:
        source = f.read()

    # 3) LEXER
    print("--- Analisis Lexico (Lexer) ---")
    tokenizer = Tokenizer(source)
    tokens = tokenizer.tokenize()
    print("Tokens reconocidos:")
    for t in tokens:
        print(t)

    # 4) PARSER
    print("\n--- Analisis Sintactico (Parser) ---")
    parser = Parser(tokens)
    try:
        ast = parser.parse()
        print("Sintaxis correcta. AST construido.")
        print("Contenido del AST (preview JSON):")
        print(json.dumps(ast, indent=4, ensure_ascii=False))
    except (SyntaxError, NameError) as e:
        print("Error en la sintaxis:", e)
        sys.exit(2)

    # 5) VALIDACIÓN MÍNIMA
    errs = validate_min(ast)
    if errs:
        print("\n--- Validación mínima ---")
        for e in errs:
            print(" -", e)
        sys.exit(3)
    else:
        print("Validación mínima: OK")

    # 6) Guardar el árbol
    try:
        with open(ast_out, 'w', encoding='utf-8') as f:
            f.write(pretty_ast(ast) + "\n")
        print("AST legible guardado en '%s'" % ast_out)
    except Exception as e:
        print("Error al guardar:", e)
        sys.exit(2)



