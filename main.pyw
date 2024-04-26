import pygame_textinput
import pygame

#relative path
import sys,os
def resource_path(relative_path):
    """Get absolute path to resource for PyInstaller"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath('.')
    return os.path.join(base_path,relative_path)

pygame.init()

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 500
FONT = pygame.font.Font(resource_path("Miracode.ttf"), 18)  # freesansbold.ttf

textinput = pygame_textinput.TextInputVisualizer(
    font_object=FONT,
    font_color=(240, 240, 240),
    cursor_blink_interval=500,
    cursor_color=(200, 200, 200)
)

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),pygame.RESIZABLE)
CLOCK = pygame.time.Clock()

vars = ['A']
exp = ''
nvars = 1
res = ['0']*(2**nvars)
isvalid = False
bksphold = False
larrhold = False
rarrhold = False
holdbuff = 1


def draw_text(text, x, y, color=(240, 240, 240)):
    txt = FONT.render(text, True, color)
    SCREEN.blit(txt, (x, y))


def rep(old, new):
    global exp
    exp = exp.replace(old, new)


def eval_exp(inputs,expression):
    rexp = expression
    for i in range(len(rexp) - 1):
        if rexp[i].isupper() and rexp[i + 1].isupper():
            return '_'
    for i in range(len(inputs)):
        rexp = rexp.replace(vars[i], inputs[i])
    try:
        return str(int(bool(eval(rexp))))
    except (NameError, SyntaxError,TypeError):
        return '_'

def find_all(st, sub):
    start = 0
    while True:
        start = st.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub) #+=1 for overlapping

while True:
    events = pygame.event.get()

    if bksphold or larrhold or rarrhold:
        textinput.cursor_blink_interval = 116
        if holdbuff%7==0:
            if bksphold:
                textinput.value = textinput.value[:-1]
            if larrhold:
                textinput.manager.cursor_pos -= 1 if textinput.manager.cursor_pos>0 else 0
            if rarrhold:
                textinput.manager.cursor_pos += 1 if textinput.manager.cursor_pos<len(textinput.value) else 0
        holdbuff+=1

    textinput.update(events)

    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.VIDEORESIZE:
            SCREEN_HEIGHT = event.h
            SCREEN_WIDTH = event.w
            SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),pygame.RESIZABLE)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_BACKSPACE: bksphold = False
            if event.key == pygame.K_LEFT: larrhold = False
            if event.key == pygame.K_RIGHT: rarrhold = False
            textinput.cursor_blink_interval = 500
            holdbuff = 1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE: bksphold = True
            if event.key == pygame.K_LEFT: larrhold = True
            if event.key == pygame.K_RIGHT: rarrhold = True
            # update
            exp = textinput.value
            rep('NOR','nor')
            rep('nor', '$$$')
            rep('NAND','nand')
            rep('nand', '&&&')

            rep('NOT', 'not')
            rep('AND', 'and')
            rep('XOR', 'xor')
            rep('OR', 'or')

            rep('!', 'not')
            rep('.', 'and')
            rep('+', 'or')
            rep('xor', '^')

            rep('not', ' not ')
            rep('and', ' and ')
            rep('or', ' or ')

            for ind in list(find_all(exp,'$$$')):
                brA = 0
                flagA = False
                operAr = ind
                operAl = ind-1
                while operAl>=0 and (not flagA or brA != 0):
                    if exp[operAl] == ')': 
                        brA += 1
                        flagA = True
                    elif exp[operAl] == '(': 
                        brA -= 1
                    operAl-=1
                operAl+=1

                brB = 0
                flagB = False
                operBl = ind + 3
                operBr = ind + 3
                while operBr<len(exp) and (not flagB or brB != 0):
                    if exp[operBr]=='(':
                        flagB = True
                        brB += 1
                    elif exp[operBr]==')':
                        brB -= 1
                    operBr+=1
                if brA != 0 or flagA == False or brB != 0 or flagB == False: break
                rep(exp[operAl:operBr],f"(not ({exp[operAl:operAr]} or {exp[operBl:operBr]}))")

            for ind in list(find_all(exp,'&&&')):
                brA = 0
                flagA = False
                operAr = ind
                operAl = ind-1
                while operAl>=0 and (not flagA or brA != 0):
                    if exp[operAl] == ')': 
                        brA += 1
                        flagA = True
                    elif exp[operAl] == '(': 
                        brA -= 1
                    operAl-=1
                operAl+=1

                brB = 0
                flagB = False
                operBl = ind + 3
                operBr = ind + 3
                while operBr<len(exp) and (not flagB or brB != 0):
                    if exp[operBr]=='(':
                        flagB = True
                        brB += 1
                    elif exp[operBr]==')':
                        brB -= 1
                    operBr+=1
                if brA != 0 or flagA == False or brB != 0 or flagB == False: break
                rep(exp[operAl:operBr],f"(not ({exp[operAl:operAr]} and {exp[operBl:operBr]}))")

            while '  ' in exp:
                rep('  ', ' ')

            # get nvars
            seen = set()
            vars = [c for c in exp if c.isupper() and not (c in seen or seen.add(c))]
            nvars = len(vars)
            if nvars == 0:
                nvars = 1
                vars = ['A']
            
            # get res
            res = ['_']*(2**nvars)
            isvalid = True
            for i in range(2**nvars):
                lst = list(format(i, f"0{nvars}b"))
                res[i] = str(eval_exp(lst,exp))
                if res[i] == '_': isvalid = False

            print(f"{exp=} {vars=} {isvalid=}")

    SCREEN.fill((30, 30, 30))

    SCREEN.blit(textinput.surface, (20, 10))

    pygame.draw.line(SCREEN,
        (20, 200, 20) if isvalid else (200, 20, 20),
        (20, 40), (SCREEN_WIDTH-20, 40)
    )

    hdiff = (SCREEN_WIDTH-40)/(nvars+1)
    vdiff = (SCREEN_HEIGHT-70)/(2**nvars+1)
    # grid
    for i in range(nvars+2):
        pygame.draw.line(SCREEN, (240, 240, 240), (20+hdiff*i,50), (20+hdiff*i, SCREEN_HEIGHT-20))
    for i in range(2**nvars+2):
        pygame.draw.line(SCREEN, (240, 240, 240),(20, 50+vdiff*i), (SCREEN_WIDTH-20, 50+vdiff*i))
    # text
    for i in range(nvars+1):
        draw_text('X' if i == nvars else vars[i], 
            20+hdiff*(i+0.45), 45+vdiff*0.25,
            (19, 201, 255) if i == nvars else (240, 240, 240)
        )
    for i in range(2**nvars):
        lst = list(format(i, f"0{nvars}b"))
        for j in range(nvars+1):
            draw_text(res[i] if j == nvars else lst[j], 
                20+hdiff*(j+0.45), 45 + vdiff*(i+1.25), 
                (19, 201, 255) if j == nvars else (240, 240, 240)
            )

    CLOCK.tick(30)
    pygame.display.update()
    pygame.display.set_caption('Truth Table Generator | ') # + str(round(CLOCK.get_fps(), 1))
