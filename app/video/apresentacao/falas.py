"""Texto final das 15 falas (fonte única). A legenda do vídeo é a própria fala.

`|` marca quebra de linha e `||` troca de página na legenda; a voz recebe o texto sem esses sinais.
"""

FALAS = {
    "01": "Bruno, esse é o BK Gestão: | o estoque e as vendas da loja, || no teu celular.",
    "02": "Abriu, tu já vê quanto vendeu hoje | e o que precisa de atenção: || peça esgotada, acabando ou parada.",
    "03": "No estoque, cada peça mostra | a quantidade por tamanho. || O que está faltando | aparece em vermelho.",
    "04": "Para achar uma peça, é só digitar | o nome, a marca ou a cor.",
    "05": "Dentro da peça, tu ajusta | cada tamanho, vê a margem || e quanto tempo o estoque dura | no ritmo de venda.",
    "06": "Para vender, toca na peça, | escolhe o tamanho e cobra.",
    "07": "Vendeu, o estoque baixa sozinho. || E o aplicativo avisa quando | um tamanho esgota.",
    "08": "O comprovante já sai pronto | para mandar no WhatsApp do cliente.",
    "09": "Com o site ligado, | o pedido de lá aparece aqui. || Confirmou o pagamento, | virou venda.",
    "10": "Chegou mercadoria? Tu dá entrada | por tamanho, em poucos toques.",
    "11": "Peças paradas há mais de | quarenta e cinco dias || viram uma oferta pronta | para o grupo VIP.",
    "12": "A lista do que pedir | ao fornecedor se monta sozinha, || com base no que mais vende.",
    "13": "No resumo, tu acompanha | as vendas, o lucro estimado || e as formas de pagamento | do período.",
    "14": "E no fim do dia, | o fechamento sai em um toque.",
    "15": "Tudo isso feito para a BK, | com as tuas peças, no teu celular.",
}


def falada(n):
    """Texto que vai para a voz (sem marcas de quebra)."""
    return " ".join(FALAS[n].replace("||", " ").replace("|", " ").split())


def paginas(n):
    """Lista de páginas; cada página é lista de linhas."""
    return [[l.strip() for l in p.split("|") if l.strip()] for p in FALAS[n].split("||")]


if __name__ == "__main__":
    import json, sys
    if "--json" in sys.argv:
        print(json.dumps({n: falada(n) for n in FALAS}, ensure_ascii=False, indent=1))
    else:
        tot = 0
        for n in FALAS:
            t = falada(n)
            tot += len(t.split())
            print(n, len(t.split()), t)
        print("palavras:", tot)
