#Calc
import sys
import math
import time
import board
import keypad
import displayio
import framebufferio
import picodvi
import terminalo
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font

displayio.release_displays()
try:
    fb = picodvi.Framebuffer(
        400, 240,
        clk_dp=board.CKP, clk_dn=board.CKN,
        red_dp=board.DOP, red_dn=board.DON,
        green_dp=board.D1P, green_dn=board.D1N,
        blue_dp=board.D2P, blue_dn=board.D2N
        color_depth=8
    )
except ValueError as e:
    print("Framebuffer init failed:", e)
    sys.exit(e)

display = framebufferio.FramebufferDisplay(fb)
main_group = displayio.Group()
display.root_group = main_group
expr_label = label.Label(terminalo.FONT, text="", scale=3,  color=0xFFFFFF, x=10, y=40)
mem_label = label.Label(terminalo.FONT, text="", scale=3, color=0xFFFFFF, x=10, y=80)
main_group.append(expr_label)
main_group.append(mem_label)

#keys rmbr to chane if i frgt

row_pins = (board.D4, board.D5, board.D6, board.D9, board.D10)
col_pins = (board.D11, board.D12, board.D13, board.D24)
km = keypad.KeyMatrix(row_pins, col_pins, columns_to_anodes=False)
keymap = [
     ["x",     "^",  "root", "/"],
     ["7",     "8",  "9",    "*"],
     ["4",     "5",  "6",    "-"],
     ["1",     "2",  "3",    "+"],
     ["clear", "0",  ".",    "sum"],
]
OPS = {"^", "root", "/", "*", "-", "+"}
tokens = []
cur_num = ""
x_mem = None
clear_clicks = 0
CLICK_WINDOW = 0.6

def fmt_num(n):
    return str(int(n)) if n == int(n) else str(n)

DISPlay_symbols = {"*": "X", "/": DIV_CHAR, "root": ROOT_CHAR}
def token_str(t):
    if t == "x":
        return "X"
    if t in OPS:
        Return DISPlay_symbols.get(t, t)
    return fmt_num(t)
def render():
    return " ".join(token_str(t) for t in tokens + ([cur_num] if cur_num else []))
def update_display(message=""):
    expr_label.text = render()[-18:]
    if message:
        mem_label.text = message
    else:
        mem_label.text = "" if x_mem is None else "x=" + fmt_num(x_mem)

def flush_num():
    global cur_num
    if cur_num:
        tokens.append(float(cur_num))
        cur_num = ""
def reset_expr():
    global tokens,cur_num
    tokens = []
    cur_num = ""
def apply_op(a, op, b):
    if op == "+":
        return a + b
    if op == "-":
        return a - b
    if op == "*":
        return a * b
    if op == "/":
        return a / b
    if op == "^":
        return a ** b
    if op == "root":
        return b ** (1/a)
def evaluate():
    flush_num()
    if not tokens:
        return None
    if len(tokens) == 2 and tokens[0] == "x" and isinstance(tokens[1], float):
        return ("assign", tokens[1])
 
    vals = []
    for t in tokens:
        if t == "x":
            if x_value is None:
                return ("error", "x undef")
            vals.append(x_value)
        else:
            vals.append(t)
 
    if len(vals) % 2 == 0:
        return ("error", "incomplete")
    
    result = vals[0]
    i = 1
    while i < len(vals):
        result = apply_op(result, vals[i], vals[i+1])
        i += 2
    return ("result", result)
update_display()
clear_clicks = 0
clear_clicksw = 0.0
while True:
    ev = km.events.get()
    if ev and ev.pressed:
        r, c = divmod(ev.keynumber, len(col_pins))
        key = keymap[r][c]
        now = time.monotonic()
        if key == "clear":
            if now - clear_clicksw < CLICK_WINDOW:
               clear_clicks = 0
               clear_clicksw = now
            clear_clicks += 1
            if clear_clicks >= 1:
                reset_expr()
            if clear_clicks >= 3:
                x_value = None
                clear_clicks = 0
                update_display("Cleared x")
            else:
                update_display("")
        elif key == "x":
            flush_num()
            tokens.append("x")
            update_display(render())
        elif key in OPS:
            flush_num()
            tokens.append(key)
            update_display(render())
        elif key == ".":
            if "." not in cur_num:
                cur_num += "."
                update_display(render())
        elif key == "sum":
            result = evaluate()
            if result is None:
                update_display("")
            elif result[0] == "error":
                update_display(result[1])
            elif result[0] == "assign":
                x_value = result[1]
                update_display("x=" + fmt_num(x_value))
                reset_expr()
            else:
                update_display(fmt_num(result[1]))
                reset_expr()
            reset_expr()
        else:
            cur_num += key
            update_display(render())
    time.sleep(0.01)
        



