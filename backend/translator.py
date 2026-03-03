import ast


# ----------------------------
# Expression Handling
# ----------------------------

def expr_to_java(expr):

    if isinstance(expr, ast.BinOp):
        return f"{expr_to_java(expr.left)} {op_to_java(expr.op)} {expr_to_java(expr.right)}"

    if isinstance(expr, ast.Compare):
        left = expr_to_java(expr.left)
        right = expr_to_java(expr.comparators[0])
        op = compare_to_java(expr.ops[0])
        return f"{left} {op} {right}"

    if isinstance(expr, ast.Name):
        return expr.id

    if isinstance(expr, ast.Constant):
        if isinstance(expr.value, str):
            return f"\"{expr.value}\""
        return str(expr.value)

    if isinstance(expr, ast.Call):
        if isinstance(expr.func, ast.Name) and expr.func.id == "print":
            args = ", ".join(expr_to_java(a) for a in expr.args)
            return f"System.out.println({args})"

    raise NotImplementedError(f"Unsupported expression: {type(expr)}")


def op_to_java(op):
    if isinstance(op, ast.Add): return "+"
    if isinstance(op, ast.Sub): return "-"
    if isinstance(op, ast.Mult): return "*"
    if isinstance(op, ast.Div): return "/"
    if isinstance(op, ast.Mod): return "%"
    raise NotImplementedError


def compare_to_java(op):
    if isinstance(op, ast.Gt): return ">"
    if isinstance(op, ast.Lt): return "<"
    if isinstance(op, ast.Eq): return "=="
    if isinstance(op, ast.NotEq): return "!="
    if isinstance(op, ast.GtE): return ">="
    if isinstance(op, ast.LtE): return "<="
    raise NotImplementedError


# ----------------------------
# Statement Handling
# ----------------------------

def stmt_to_java(stmt, indent=8):
    space = " " * indent

    if isinstance(stmt, ast.Assign):
        target = stmt.targets[0].id
        value = expr_to_java(stmt.value)
        return f"{space}int {target} = {value};"

    if isinstance(stmt, ast.Return):
        return f"{space}return {expr_to_java(stmt.value)};"

    if isinstance(stmt, ast.Expr):
        return f"{space}{expr_to_java(stmt.value)};"

    if isinstance(stmt, ast.If):
        code = f"{space}if ({expr_to_java(stmt.test)}) {{\n"
        for s in stmt.body:
            code += stmt_to_java(s, indent + 4) + "\n"
        code += f"{space}}}"

        if stmt.orelse:
            code += " else {\n"
            for s in stmt.orelse:
                code += stmt_to_java(s, indent + 4) + "\n"
            code += f"{space}}}"

        return code

    if isinstance(stmt, ast.For):
        if isinstance(stmt.iter, ast.Call) and stmt.iter.func.id == "range":
            start = expr_to_java(stmt.iter.args[0])
            end = expr_to_java(stmt.iter.args[1])
            var = stmt.target.id

            code = f"{space}for (int {var} = {start}; {var} < {end}; {var}++) {{\n"
            for s in stmt.body:
                code += stmt_to_java(s, indent + 4) + "\n"
            code += f"{space}}}"
            return code

    raise NotImplementedError(f"Unsupported statement: {type(stmt)}")


# ----------------------------
# Function Handling
# ----------------------------

def function_to_java(func):

    name = func.name
    params = ", ".join(f"int {arg.arg}" for arg in func.args.args)

    code = f"    public static int {name}({params}) {{\n"

    for stmt in func.body:
        code += stmt_to_java(stmt) + "\n"

    code += "    }\n"

    return code


# ----------------------------
# Entry Point
# ----------------------------

def translate_python_to_java(code):
    try:
        tree = ast.parse(code)

        java_code = ""

        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                java_code += function_to_java(node) + "\n"

        return java_code.strip()

    except Exception:
        return "// Waiting for valid Python code..."