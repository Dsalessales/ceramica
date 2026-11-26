# -*- coding: utf-8 -*-
"""Troca os textos do template Handsel pelos textos do ateliê da Raquel Rocha.

Uso (na raiz do repositório):  python3 tools/raquel_textos.py
Aplica as trocas no index.html e nos scripts do Framer (.mjs), que recriam a página.
Pode ser rodado mais de uma vez: só troca o que ainda está em inglês.
"""
import glob, html, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITES = os.path.join(ROOT, 'assets/framerusercontent.com/sites/5Rfp7hj7qu9mBkKNuzoZov')
PAGE = 'EZAeT3pfwzaGoKFcJIPo3JEW6q9tcY26lMvvRQyiaJA.dXHrTmft.mjs'
RING = 'RingReveal.BwXoQHqz.mjs'
TOP = 'toplevel-deps.CfpaRyEM.mjs'
BASE = '/ceramica'
RESERVAR = BASE + '/reservar/'
INSTA = 'https://instagram.com/rrochaceramica'

# Frases longas: trocadas como trecho de texto, em qualquer arquivo.
SUB = [
    # Legendas dos depoimentos (antes dos nomes das oficinas)
    ('Wheel Throwing II · a set of four bowls', 'Oficina de Casal'),
    ('Introduction to Linocut · two-colour print', 'Oficina em família'),
    ('Frame Loom Weaving · wall hanging', 'Oficina infantil'),
    ('Silver Ring Making · hammered band', 'Aula noturna'),
    # SEO
    ('Handsel — Creative Workshop & Pottery Studio Framer Template', 'Raquel Rocha Cerâmica — Oficinas de cerâmica em Cunha'),
    ('Handsel — Creative Workshop &amp; Pottery Studio Framer Template', 'Raquel Rocha Cerâmica — Oficinas de cerâmica em Cunha'),
    ('Handsel is a premium Framer template for craft studios and creative workshops, with CMS classes, dated sessions, tutors, a journal, booking requests and gift cards.',
     'Oficinas de modelagem manual em Cunha, SP: casal, família, crianças e aula noturna. Reserve o horário e pague o sinal no Pix.'),

    # Hero
    ('© Since 2014 · Bristol', 'Cerâmica artesanal · Cunha, SP'),
    ('Made by hand,', 'Feito à mão,'),
    ('four ways,', 'a dois ou em família,'),
    ('one bench at a time.', 'uma peça por vez.'),
    ('★★★★★  4.9 / 5', 'Modelagem manual'),
    ('320 students this year', 'Oficinas das 10h às 17h'),
    ('Wednesday, November 11', 'Sábado, 28 de novembro'),
    ('Friday, November 13', 'Domingo, 29 de novembro'),
    ('Saturday, November 14', 'Sábado, 5 de dezembro'),
    ('November 11', 'Sáb, 28 nov'),
    ('06:30 PM', '14h00'),
    ('From £340', 'Sinal de 50%'),
    ('From £320', 'Sinal de 50%'),
    ('From £95', 'Sinal de 50%'),
    ('£340', '1h30'),

    # Ateliê
    ('Ceramics · Printmaking · Textiles · Jewellery', 'Família · Casal · Infantil · Noturna'),
    ('Four crafts, one studio', 'Quatro oficinas, um ateliê'),
    ('Four crafts', 'Quatro oficinas'),
    ('one studio,', 'um ateliê,'),
    ('endless ways', 'a mesma argila'),
    ('to begin.', 'nas mãos.'),
    ('Clay being shaped by hand', 'Argila sendo modelada à mão'),
    ('● Bristol, since 2014', '● Cunha, SP'),
    ('Every piece here starts', 'Toda peça aqui começa'),
    ('with a pair of hands.', 'com um par de mãos.'),
    ('Handsel is a working studio where people learn with their hands. Small groups, makers who still make, and every tool you need on the bench. Come for an afternoon, stay for a season.',
     'O ateliê da Raquel Rocha é um lugar para colocar as mãos no barro. Turmas pequenas, modelagem manual e tudo o que você precisa na mesa. Venha a dois, em família ou sozinho, e leve para casa a peça que você fez.'),
    ('Meet the studio', 'Conheça o ateliê'),

    # Oficinas (01 Família, 02 Casal, 03 Infantil, 04 Noturna)
    ('01  Ceramics', '01  Família'),
    ('02  Printmaking', '02  Casal'),
    ('03  Textiles', '03  Infantil'),
    ('04  Jewellery', '04  Noturna'),
    ('No. 01 · 3 classes · 1 tutor', 'Nº 01 · 1h30 · com a Raquel'),
    ('No. 02 · 3 classes · 1 tutor', 'Nº 02 · 1h30 · com a Raquel'),
    ('No. 03 · 3 classes · 1 tutor', 'Nº 03 · 1h30 · com a Raquel'),
    ('No. 04 · 3 classes · 1 tutor', 'Nº 04 · 1h30 · com a Raquel'),
    ('3 classes · 1 tutor', '1h30 · com a Raquel'),
    ('Ash-glazed bottle vase · made in Wheel Throwing II', 'Vaso modelado à mão · feito na oficina Avós e netos'),
    ('Wheel, hand-building and glazing in a studio with six wheels and two kilns. Start with a taster, stay for the firing.',
     'Pais, filhos e avós na mesma mesa. Cada um modela a sua peça, com a Raquel guiando do primeiro toque no barro ao acabamento.'),
    ('Wheel Throwing II', 'Avós e netos'),
    ('Wheel Throwing I', 'Oficina em família'),
    ('Mugs on the Wheel', 'Turma de amigos'),
    ('See all ceramics classes', 'Reservar oficina em família'),
    ('Carved lino block and ink roller', 'Peça de cerâmica feita a dois'),
    ('Two-colour linocut, edition of 12 · made in Introduction to Linocut', 'Vaso feito a quatro mãos · feito na Oficina de Casal'),
    ('Linocut, screen printing and risograph on presses you can book once you have done your first class.',
     'Uma tarde no barro a dois. Cada um modela a sua peça, lado a lado, e vocês levam para casa a lembrança desse dia.'),
    ('Introduction to Linocut', 'Tarde a dois'),
    ('Screen Printing I', 'Oficina de Casal'),
    ('Botanical Lino Prints', 'Vale-presente de casal'),
    ('See all printmaking classes', 'Reservar oficina de casal'),
    ('Skeins of naturally dyed yarn', 'Peça de cerâmica feita por criança'),
    ('Indigo shibori cloths · made in Natural Dyeing', 'Primeira peça · feita na Oficina Infantil'),
    ('Weaving, natural dyeing and embroidery, with plant-dyed yarn from our own dye garden.',
     'Modelagem pensada para crianças, sempre com um adulto junto e argila de sobra para explorar.'),
    ('Frame Loom Weaving', 'Primeira peça'),
    ('Natural Dyeing', 'Criança + acompanhante'),
    ('Indigo Shibori', 'Festa no ateliê'),
    ('See all textiles classes', 'Reservar oficina infantil'),
    ('Handmade silver rings', 'Peça de cerâmica feita à noite'),
    ('Stacking rings in silver and brass · made in Silver Ring Making', 'Tigela modelada à mão · feita na Aula noturna'),
    ('Ring making, stone setting and casting at fully equipped benches, from your very first silver band.',
     'A oficina depois do expediente, com luz baixa e tempo para se concentrar no barro.'),
    ('Silver Ring Making', 'Aula noturna'),
    ('Stone Setting', 'Noite a dois'),
    ('Hammered Stacking Rings', 'Turma fechada'),
    ('See all jewellery classes', 'Reservar aula noturna'),

    # Próximas vagas
    ('New dates every Monday', 'Horários das 10h às 17h'),
    ('Starting soon.', 'Próximas vagas.'),
    ('All classes', 'Reservar'),

    # Do barro à mesa
    ('Buff stoneware with fine grog, wedged by hand and rolled into an even slab.', 'A argila é sovada à mão e preparada na mesa antes de você começar.'),
    ('Pressed over a plaster mould, then trimmed on the wheel once leather-hard.', 'Você modela a sua peça com as mãos, com a Raquel guiando cada passo.'),
    ('Bisque fired, then dipped twice in a pale ash glaze and wiped at the foot.', 'A peça seca no ateliê e passa pela primeira queima e pelo esmalte.'),
    ('A second firing to 1260°C melts the glaze into glass. Ready for the table.', 'Na queima de alta temperatura, o esmalte vira vidro. Pronta para a mesa.'),
    ('Week 2–3', 'Etapa 2'),
    ('Week 1', 'Etapa 1'),
    ('Week 4', 'Etapa 3'),
    ('Week 5', 'Etapa 4'),
    ('07 — Made at Handsel', '07 — Feito no ateliê'),
    ('Made here, taken home.', 'Feito aqui, levado para casa.'),
    ('From clay to table', 'Do barro à mesa'),
    ('Bisque and glaze', 'Biscoito e esmalte'),
    ('Final firing', 'Queima final'),
    ('Yours to keep', 'Para você levar'),
    ('Made at Handsel', 'Feito no ateliê'),
    ('Ash-glazed bowl', 'Tigela modelada à mão'),
    ('Clay to table', 'Do barro à mesa'),
    ('Bisque + glaze', 'Biscoito + esmalte'),
    ('1260°C', 'Alta temp.'),

    # Jeitos de começar
    ('Workshops · Courses · Membership', 'Oficina · Presente · Turma fechada'),
    ('Three ways in.', 'Três jeitos de começar.'),
    ('Try it for an afternoon, learn it over six weeks, or make the studio yours with a membership.',
     'Venha para uma tarde no barro, dê a experiência de presente ou feche o ateliê só para o seu grupo.'),
    ('A few hours to try something new.', 'Uma tarde para colocar as mãos no barro.'),
    ('3 hours · up to 8 people · materials included', '1h30 · casal, família ou crianças · material incluso'),
    ('from £85', 'Sinal 50%'),
    ('Time to build a practice, one week at a time.', 'Uma oficina de presente para quem você ama.'),
    ('6 evenings · same tutor · keep what you make', 'válido por 6 meses · quem ganha escolhe a data'),
    ('Bench time for your own work, any day.', 'O ateliê só para o seu grupo, aniversário ou equipe.'),
    ('6 days a week · glazes and firing included', 'data combinada · até a capacidade do ateliê'),
    ('Members save 10% on every workshop and course.', 'Reserve online e garanta o horário com o sinal no Pix.'),
    ('Compare memberships', 'Ver horários'),

    # Dentro do ateliê
    ('Inside Handsel', 'Dentro do ateliê'),
    ('Open seven days a week', 'Oficinas das 10h às 17h'),
    ('A place to find', 'Um lugar para'),
    ('your practice.', 'desacelerar.'),
    ('Shared tables, well-used tools and room to try. Come for one evening, or keep a shelf here for years.',
     'Mesa compartilhada, argila fresca e tempo para errar e recomeçar. Você sai com uma peça feita pelas suas mãos.'),
    ('crafts under one roof', 'oficinas no mesmo ateliê'),
    ('people per class, at most', 'casais por dia, em média'),
    ('wheels, two kilns, three presses', 'de oficina, do barro à peça'),
    ('Bring your people.', 'Grupos.'),
    ('Plan a group', 'Fechar turma'),
    ('See you at the bench', 'Te espero no ateliê'),
    ('Your first piece starts here.', 'Sua primeira peça começa aqui.'),
    ('Find a class', 'Reservar oficina'),
    ('Give a gift card', 'Dar de presente'),

    # Quem conduz
    ('Four makers, one bench each', 'Uma ceramista, quatro oficinas'),
    ('The people at the bench.', 'Quem te recebe.'),
    ('The people', 'Quem te'),
    ('at the bench.', 'recebe.'),
    ('Every class is taught by someone who still makes for a living, in small groups of eight or fewer.',
     'Todas as oficinas são conduzidas pela Raquel Rocha, ceramista em Cunha, com turmas pequenas.'),
    ('Meet the team', 'Conheça a Raquel'),
    ('Head of ceramics', 'Oficina em família'),
    ('Printmaker', 'Oficina de casal'),
    ('Dyer and weaver', 'Oficina infantil'),
    ('Silversmith', 'Aula noturna'),
    ('Mara Ellison', 'Raquel Rocha'),
    ('Tomas Reyes', 'Raquel Rocha'),
    ('Ada Okafor', 'Raquel Rocha'),
    ('Peter Lund', 'Raquel Rocha'),

    # Depoimentos (exemplos, para trocar pelos reais)
    ('From our students', 'Depoimentos'),
    ('In their own words.', 'Quem já veio.'),
    ('4.9 average from 320 student reviews', 'Depoimentos de exemplo'),
    ('I came in thinking I wasn’t creative. Six weeks later I had made a full set of bowls for my own kitchen.',
     'Espaço para o depoimento de um casal que fez a oficina (texto de exemplo).'),
    ('The best Saturday I have had in years. Phones away, hands inky, tea on the bench.',
     'Espaço para o depoimento de uma família que veio ao ateliê (texto de exemplo).'),
    ('At sixty I finally learned to weave. Ada made every single row feel possible.',
     'Espaço para o depoimento de quem trouxe as crianças (texto de exemplo).'),
    ('Peter is the calmest teacher I have met. I wear the ring I made every day.',
     'Espaço para o depoimento de quem fez a aula noturna (texto de exemplo).'),
    ('Priya Nair', 'Nome do casal'),
    ('Tom Becker', 'Nome da família'),
    ('Margaret Ellis', 'Nome do responsável'),
    ('Daniel Kim', 'Nome do aluno'),

    # Dúvidas
    ('Booking · Classes · Membership · Gifts', 'Reserva · Oficinas · Turmas · Presente'),
    ('Good to know before you come.', 'Bom saber antes de vir.'),
    ('Good to know', 'Bom saber'),
    ('before you come.', 'antes de vir.'),
    ('Booking, cancelling, what to wear and how membership works. If your question is not here, we answer every email within a day.',
     'Reserva, remarcação, o que vestir e como funciona o vale-presente. Se a sua dúvida não estiver aqui, é só chamar no Instagram.'),
    ('Still wondering?', 'Ainda com dúvida?'),
    ('Contact the studio', 'Falar com a Raquel'),
    ('Pick a date on any class page and send a request. We reply by email within one working day, and your place is confirmed once we hear back.',
     'Escolha a oficina, o dia e o horário, e pague o sinal de 50% no Pix. A vaga é confirmada na hora, sem troca de mensagens.'),
    ('How do I book a class?', 'Como faço para reservar?'),
    ('Yes, up to 72 hours before the class. Move to another date for free, or keep the full amount as studio credit.',
     'Pode remarcar sem custo até 48 horas antes. Depois disso, o sinal não é devolvido.'),
    ('Can I cancel or move my booking?', 'Posso remarcar ou cancelar?'),
    ('None for workshops. Each course page says what you should know before the first session.',
     'Nenhuma. A Raquel conduz cada passo, do primeiro toque no barro ao acabamento.'),
    ('Do I need any experience?', 'Preciso saber modelar?'),
    ('Clothes you do not mind getting clay, ink or dye on. Aprons, tools and materials are provided.',
     'Roupa confortável, que possa sujar de argila. Aventais, ferramentas e material ficam por conta do ateliê.'),
    ('What should I wear?', 'Que roupa devo usar?'),
    ('Classes are for ages 16 and up. Family workshops run on selected Sundays.',
     'Crianças participam da Oficina Infantil e da Oficina em Família, sempre com um adulto junto.'),
    ('Is there an age limit?', 'Crianças podem participar?'),
    ('Monthly, cancel any time. Bench time six days a week, with glazes and firing included.',
     'Pode. Aniversários, amigos ou equipes: escolha a data e a gente combina os detalhes.'),
    ('How does membership work?', 'Dá para fechar uma turma só para o meu grupo?'),
    ('Yes, for any amount or a specific class. Gift cards are valid for twelve months.',
     'Sim. O vale-presente vale por 6 meses e quem ganha escolhe a data depois.'),
    ('Do you sell gift cards?', 'Vocês têm vale-presente?'),

    # Instagram
    ('● On the bench this week', '● No ateliê esta semana'),
    ('Fresh off the wheel,', 'Saindo do forno,'),
    ('the press and the loom.', 'direto das mãos de quem fez.'),
    ('Follow the bench · @handsel.studio · ', 'Siga o ateliê · @rrochaceramica · '),
    ('Follow the bench', 'Siga o ateliê'),
    ('Recent work from the Handsel studio', 'Peças recentes do ateliê'),
    ('Follow on Instagram', 'Seguir no Instagram'),
    ('View post', 'Ver post'),
    ('hello@handsel.studio', '@rrochaceramica'),
    ('mailto:hello@handsel.studio', 'https://instagram.com/rrochaceramica'),
    ('@handsel.studio', '@rrochaceramica'),

    # Rodapé
    ('Stokes Croft, Bristol BS1 3QY', 'Cunha · SP'),
    ('18 Kiln Yard', 'Ateliê R Rocha'),
    ('https://maps.google.com/?q=18+Kiln+Yard+Stokes+Croft+Bristol', 'https://maps.google.com/?q=Cunha+SP'),
    ('Get directions', 'Como chegar'),
    ('Mon–Fri 9:00–21:00', 'Oficinas das 10h às 17h'),
    ('Sat–Sun 10:00–18:00', 'Com hora marcada'),
    ('+44 117 000 0000', 'Reserve pelo site'),
    ('Come and make something.', 'Venha fazer a sua peça.'),
    ('New dates, open studio evenings and the odd kiln opening. One email a month, never more.',
     'Novos horários, datas especiais e aberturas de forno. Um e-mail por mês, no máximo.'),
    ('I agree to the Privacy Policy', 'Concordo com a Política de Privacidade'),
    ('Enable JavaScript to submit this form.', 'Ative o JavaScript para enviar.'),
    ('© 2026 Handsel Studio', '© 2026 Raquel Rocha Cerâmica'),
    ('Browse classes', 'Reservar oficina'),
    ('Makers at work in the Handsel studio', 'Mãos no barro no ateliê'),
    ('Handmade stoneware vase', 'Vaso de cerâmica feito à mão'),
]

# Palavras curtas: trocadas só quando são o texto inteiro (`Palavra` no .mjs, >Palavra< no HTML).
EXACT = [
    ('Ceramics', 'Família'), ('Printmaking', 'Casal'), ('Textiles', 'Infantil'), ('Jewellery', 'Noturna'),
    ('Email address', 'Seu e-mail'),
    ('3 classes', '1h30'), ('6 weeks', '1h30'), ('3 hrs', '1h30'),
    ('One day', '1h30'), ('Six weeks', '1h30'), ('Four weeks', '1h30'),
    ('Clay', 'Argila'), ('Shape', 'Forma'), ('Glaze', 'Secagem'), ('Fired', 'Queima'),
    ('5 weeks', 'Poucas semanas'), ('Firings', 'Queimas'), ('Kiln', 'Forno'), ('Maker', 'Quem fez'), ('You', 'Você'),
    ('2 firings', '2 queimas'), ('1 maker', '1 par de mãos'),
    ('The studio', 'O ateliê'), ('Disciplines', 'Oficinas'), ('Object', 'Peça'),
    ('This month', 'Esta semana'), ('Ways in', 'Por onde começar'),
    ('Workshop', 'Oficina'), ('per person', 'na reserva'),
    ('Course', 'Presente'), ('£320', 'Vale'), ('six weeks', 'presente'),
    ('Open studio', 'Turma fechada'), ('£140', 'Sob'), ('per month', 'consulta'),
    ('Made by hand', 'Feito à mão'), ('Tutors', 'Quem conduz'), ('Kind words', 'Depoimentos'),
    ('Questions', 'Dúvidas'), ('Craft studio', 'Cerâmica'), ('Handsel', 'R Rocha'),
    ('Next class', 'Próxima oficina'), ('● Next class', '● Próxima oficina'),
    ('Classes', 'Oficinas'), ('Schedule', 'Horários'), ('Private groups', 'Grupos'),
    ('Gift cards', 'Vale-presente'), ('About', 'Sobre'), ('Journal', 'Diário'), ('Visit', 'Visite'),
    ('Hours', 'Horários'), ('Contact', 'Contato'), ('Subscribe', 'Assinar'), ('Privacy', 'Privacidade'),
    ('Terms', 'Termos'), ('Thank you', 'Obrigado'), ('Try again', 'Tentar de novo'),
    ('MENU', 'MENU'), ('Menu', 'Menu'), ('Sold out', 'Esgotado'),
    ('/classes', RESERVAR), ('/gift-cards', RESERVAR + '#presente'),
    ('https://instagram.com/', INSTA), ('mailto:hello@handsel.studio', INSTA),
]
EXACT_FILES = {PAGE, RING, TOP}

# Números das estatísticas (Dentro do ateliê): trocados só perto do rótulo.
STATS = [('4', '4', 'oficinas no mesmo ateliê'), ('8', '3', 'casais por dia, em média'), ('6', '1h30', 'de oficina, do barro à peça')]


def esc(t):
    return html.escape(t, quote=False)


def fix_stats(s, is_html):
    for old, new, label in STATS:
        i = s.find(label if not is_html else esc(label))
        while i != -1:
            window_start = max(0, i - 2500)
            chunk = s[window_start:i]
            if is_html:
                pat = r'>' + re.escape(old) + r'<'
                rep = '>' + new + '<'
            else:
                pat = r'`' + re.escape(old) + r'`'
                rep = '`' + new + '`'
            ms = list(re.finditer(pat, chunk))
            if ms:
                m = ms[-1]
                s = s[:window_start + m.start()] + rep + s[window_start + m.end():]
            i = s.find(label if not is_html else esc(label), i + 1)
    return s


def apply(path, is_html, exact):
    s = open(path, encoding='utf-8').read()
    orig = s
    counts = {}
    for old, new in SUB:
        variants = {old} | ({esc(old)} if is_html else set())
        for v in variants:
            n = s.count(v)
            if n:
                s = s.replace(v, esc(new) if is_html and v != old else new)
                counts[old] = counts.get(old, 0) + n
    if exact:
        for old, new in EXACT:
            if is_html:
                pats = [('>' + esc(old) + '<', '>' + esc(new) + '<'), ('"' + old + '"', '"' + new + '"')]
                pats = [p for p in pats if not (p[0].startswith('"') and not old.startswith(('/', 'http', 'mailto')))]
            else:
                pats = [('`' + old + '`', '`' + new + '`')]
            for a, b in pats:
                n = s.count(a)
                if n:
                    s = s.replace(a, b)
                    counts[old] = counts.get(old, 0) + n
    s = fix_stats(s, is_html)
    if s != orig:
        open(path, 'w', encoding='utf-8').write(s)
    return counts


if __name__ == '__main__':
    total = {}
    c = apply(os.path.join(ROOT, 'index.html'), True, True)
    for k, v in c.items(): total[k] = total.get(k, 0) + v
    for f in sorted(glob.glob(os.path.join(SITES, '*.mjs'))):
        name = os.path.basename(f)
        c = apply(f, False, name in EXACT_FILES)
        for k, v in c.items(): total[k] = total.get(k, 0) + v
    missing = [o for o, _ in SUB if o not in total and esc(o) not in total]
    print('trocas aplicadas:', sum(total.values()))
    if missing:
        print('sem ocorrência (já trocado ou ausente):')
        for m in missing: print('  -', m)
