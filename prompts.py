prompt_strategies = {
    "zero_shot": lambda text: f"""Resuma o texto abaixo mantendo o idioma original e diminuindo a complexidade textual. Não inclua nenhuma resposta ou explicação além do resumo.
    {text}""",
    "zero_shot_with_instructions": lambda text: f"""Resuma o texto financeiro abaixo mantendo o idioma original e diminuindo a complexidade textual e seguindo estas regras:
- "em conformidade com" = "seguindo"
- "divulgado" = "informado"
- "convergência" = "ajuste"
- "remuneração dos acionistas" = "pagamento aos donos de ações"
- Números: mantenha como estão
- Datas: use formato DD/MM/AAAA

FORMATO:
- entre 3 e 6 frases no máximo.
- Cada frase com 10-15 palavras.
- Uma ideia por frase.

Texto original:
{text}""",
    "one_shot": lambda text: f"""Resuma o texto financeiro abaixo mantendo o idioma original e diminuindo a complexidade textual e seguindo estas regras:
- "em conformidade com" = "seguindo"
- "divulgado" = "informado"
- "convergência" = "ajuste"
- "remuneração dos acionistas" = "pagamento aos donos de ações"
- Números: mantenha como estão
- Datas: use formato DD/MM/AAAA

FORMATO:
- entre 3 e 6 frases no máximo.
- Cada frase com 10-15 palavras.
- Uma ideia por frase.

EXEMPLO:
Texto original: "Em conformidade com o § 4º do art. 157 da Lei nº 6.404, de 15 de dezembro de 1976, com a Resolução CVM nº 44, de 23 de agosto de 2021 e em complemento aos Fatos Relevantes divulgados em 19 de fevereiro de 2025 e 14 de agosto de 2025, o Banco do Brasil comunica que, em virtude da necessidade de convergência para o payout de 30% aprovado pela Administração em 13 de agosto de 2025, a remuneração dos acionistas referente ao terceiro trimestre de 2025 será paga integralmente em 11/12/2025, ou seja, não haverá pagamento antecipado referente ao período."
Resumo: "O Banco do Brasil informa que vai pagar os acionistas em 11/12/2025. Não haverá pagamento antes dessa data. Essa decisão segue a regra de pagar 30% do lucro aprovada em agosto de 2025."

Agora resuma o texto abaixo da mesma forma:
{text}""",
    "chain_of_thought": lambda text: f"""Resuma este texto financeiro em português seguindo este processo:
    PASSO 1 - Encontre os fatos principais:
    - Quem? (empresa, órgão)
    - O quê? (ação, decisão, resultado)
    - Quando? (datas)
    - Quanto? (valores, percentuais)

    PASSO 2 - Simplifique cada fato:
    - Troque palavras difíceis por fáceis
    - Use verbos simples (fazer, ter, ser, ir)
    - Divida frases longas em curtas

    PASSO 3 - Escreva o resumo:
    - Uma frase para cada fato principal
    - Máximo 15 palavras por frase
    - 3-6 frases no total

Agora aplique esse processo ao texto abaixo e forneça APENAS o resumo final:
{text}""",
    "role_playing": lambda text: f"""Você é um jornalista financeiro escrevendo em português para leitores iniciantes. Sua tarefa é resumir o texto em português abaixo usando:
    PÚBLICO: Pessoas sem nenhum conhecimento técnico

    SEU ESTILO:
    - Explique como se estivesse falando
    - Use "a empresa", "o banco" em vez de nomes complicados
    - Troque "aquisição" por "compra", "implementar" por "fazer"
    - Dê contexto: "caiu de X para Y" em vez de só "caiu"

    ESTRUTURA:
    - entre 3 e 6 frases no máximo.
    - Cada frase com 10-15 palavras.
    - Uma ideia por frase.

Escreva apenas o resumo referente o texto abaixo, sem introduções ou explicações:
{text}""",
}