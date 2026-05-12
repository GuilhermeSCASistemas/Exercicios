try:
    from fpdf import FPDF
    from fpdf.enums import XPos, YPos
except ImportError:
    print("fpdf2 nao instalado. Execute: pip install fpdf2")
    exit(1)

pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()

# Titulo
pdf.set_font("Helvetica", "B", 20)
pdf.cell(
    0, 15, "Relatorio Anual 2024 - SuperTechIABrazil",
    new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C"
)
pdf.ln(5)

pdf.set_font("Helvetica", "", 12)

content = [
    ("1. Sobre a Empresa",
     "A SuperTechIABrazil e uma empresa de tecnologia fundada em 2018, com sede em Sao Paulo. "
     "Atuamos em Inteligencia Artificial, Desenvolvimento de Software e Consultoria Cloud. "
     "Contamos com 320 colaboradores em Sao Paulo, Rio de Janeiro e Recife. "
     "Nossa missao e democratizar o acesso a solucoes de IA para empresas brasileiras."),

    ("2. Desempenho Financeiro 2024",
     "O faturamento da Empresa SuperTechIABrazil no ano de 2024 foi de 10 milhoes de reais, "
     "um crescimento de 35% sobre 2023, quando a empresa faturou 7,4 milhoes de reais. "
     "Receitas: SaaS de IA R$ 4,2 milhoes (42%), Consultoria R$ 3,8 milhoes (38%), "
     "Treinamentos R$ 2,0 milhoes (20%). "
     "Lucro operacional: R$ 1,8 milhao (margem 18%). EBITDA: R$ 2,3 milhoes."),

    ("3. Clientes e Mercado",
     "Em 2024 a SuperTechIABrazil encerrou o ano com 145 clientes ativos: "
     "60 pequenas empresas, 55 medias e 30 grandes corporacoes. "
     "Setores: varejo (28%), financeiro (22%), saude (18%), educacao (15%), outros (17%). "
     "Taxa de retencao: 89%. NPS: 72 pontos."),

    ("4. Produtos e Servicos",
     "Nosso principal produto e o AIFlow, plataforma de automacao com IA, 980 usuarios mensais. "
     "Planos: Starter R$ 299/mes, Professional R$ 899/mes, Enterprise consultivo. "
     "Integracao com Salesforce, HubSpot, SAP e Google Workspace. "
     "Em 2024 lancamos o DocAI para leitura de PDFs, com 120 clientes beta."),

    ("5. Equipe e Cultura",
     "320 colaboradores: 180 desenvolvedores, 45 consultores de IA, "
     "40 profissionais de vendas, 30 de atendimento, 25 administrativo. "
     "eNPS: 68 pontos. Taxa de turnover: 12% (media do setor: 18%)."),

    ("6. Metas para 2025",
     "Para 2025 a SuperTechIABrazil planeja: "
     "faturamento de R$ 15 milhoes (+50%), "
     "expansao para 5 novos estados, "
     "80 novas contratacoes, "
     "lancamento de 2 produtos de IA Generativa, "
     "certificacao ISO 27001 "
     "e inicio de operacoes internacionais em Portugal."),
]

for titulo, texto in content:
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, titulo, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(0, 7, texto.strip())
    pdf.ln(5)

pdf.output("document.pdf")
print("PDF de exemplo gerado: document.pdf")
print("   (Relatorio ficticio da empresa SuperTechIABrazil)")
