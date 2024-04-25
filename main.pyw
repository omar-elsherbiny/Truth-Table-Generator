import pygame_textinput
import pygame
pygame.init()

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 500
FONT = pygame.font.Font("Miracode.ttf", 18)  # freesansbold.ttf

textinput = pygame_textinput.TextInputVisualizer(
    font_object=FONT,
    font_color=(240, 240, 240),
    cursor_blink_interval=500,
    cursor_color=(200, 200, 200)
)

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
CLOCK = pygame.time.Clock()

vars = ['A']
exp = ''
nvars = 1
res = ['0']*(2**nvars)
isvalid = False


def draw_text(text, x, y, color=(240, 240, 240)):
    txt = FONT.render(text, True, color)
    SCREEN.blit(txt, (x, y))


def rep(old, new):
    global exp
    exp = exp.replace(old, new)


def eval_exp(inps):
    rexp = exp
    for i in range(len(rexp) - 1):
        if rexp[i].isupper() and rexp[i + 1].isupper():
            return '_'
    for i in range(len(inps)):
        rexp = rexp.replace(vars[i], inps[i])
    try:
        return str(int(bool(eval(rexp))))
    except (NameError, SyntaxError,TypeError):
        return '_'

while True:
    events = pygame.event.get()

    textinput.update(events)

    for event in events:
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            # update
            #TODO: xor not problem
            #TODO: A nor B
            #TODO: A nand B
            exp = textinput.value
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
            res = ['0']*(2**nvars)
            isvalid = True
            for i in range(2**nvars):
                lst = list(format(i, f"0{nvars}b"))
                res[i] = str(eval_exp(lst))
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
    pygame.display.set_caption('Truth Table Generator | ' + str(round(CLOCK.get_fps(), 1)))
