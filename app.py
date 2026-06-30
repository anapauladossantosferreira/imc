# app.py - Calculadora de IMC (Versão Console Pura)
# Totalmente comentado linha por linha como solicitado

# ==================== IMPORTAÇÕES ====================

import sys          # Importa a biblioteca sys para capturar argumentos passados pela linha de comando
from datetime import datetime  # Importa datetime para registrar a data e hora dos cálculos


# ==================== FUNÇÃO DE CÁLCULO DO IMC ====================

def calcular_imc(peso, altura):
    """Função responsável por calcular o IMC e retornar classificação."""
    
    # Validação da altura: não pode ser zero ou negativa
    if altura <= 0:
        raise ValueError("A altura deve ser maior que zero.")  # Levanta erro se altura for inválida
    
    # Cálculo principal do IMC usando a fórmula: peso / (altura²)
    imc = peso / (altura ** 2)
    
    # ==================== CLASSIFICAÇÃO DO IMC ====================
    # Verifica em qual faixa o IMC se encaixa (padrão OMS)
    if imc < 18.5:
        classificacao = "Abaixo do peso"   # IMC abaixo de 18.5
        emoji = "📉"
    elif imc < 25:
        classificacao = "Peso normal"      # IMC entre 18.5 e 24.9
        emoji = "✅"
    elif imc < 30:
        classificacao = "Sobrepeso"        # IMC entre 25 e 29.9
        emoji = "⚠️"
    elif imc < 35:
        classificacao = "Obesidade grau 1" # IMC entre 30 e 34.9
        emoji = "🚨"
    elif imc < 40:
        classificacao = "Obesidade grau 2" # IMC entre 35 e 39.9
        emoji = "🚨"
    else:
        classificacao = "Obesidade grau 3" # IMC 40 ou maior
        emoji = "🚨"
    
    # Retorna o IMC calculado, a classificação e o emoji
    return imc, classificacao, emoji


# ==================== FUNÇÃO PARA SALVAR HISTÓRICO ====================

def salvar_historico(peso, altura, imc, classificacao):
    """Salva cada cálculo em um arquivo de texto."""
    
    # Pega a data e hora atual no formato brasileiro
    data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    # Monta a linha que será gravada no arquivo
    linha = f"{data_hora} | Peso: {peso:.1f}kg | Altura: {altura:.2f}m | IMC: {imc:.2f} | {classificacao}\n"
    
    # Abre (ou cria) o arquivo em modo append (adiciona no final)
    with open("historico_imc.txt", "a", encoding="utf-8") as arquivo:
        arquivo.write(linha)   # Escreve a linha no arquivo
    
    print("💾 Cálculo salvo no histórico com sucesso!")


# ==================== FUNÇÃO PARA MOSTRAR HISTÓRICO ====================

def mostrar_historico():
    """Exibe todos os cálculos salvos anteriormente."""
    try:
        # Tenta abrir o arquivo de histórico
        with open("historico_imc.txt", "r", encoding="utf-8") as arquivo:
            conteudo = arquivo.read()   # Lê todo o conteúdo
            
        # Verifica se o arquivo está vazio
        if conteudo.strip() == "":
            print("📭 O histórico está vazio.")
        else:
            print("\n" + "="*70)
            print("📖 HISTÓRICO DE CÁLCULOS DE IMC")
            print("="*70)
            print(conteudo)             # Mostra todo o histórico
            print("="*70)
            
    except FileNotFoundError:
        # Caso o arquivo ainda não exista
        print("📭 Nenhum histórico encontrado ainda. Faça seu primeiro cálculo.")


# ==================== PROGRAMA PRINCIPAL ====================

# Mensagem inicial do programa
print("🧮 Calculadora de IMC - Versão Console\n")

# Verifica se o usuário digitou "--historico" como argumento
if len(sys.argv) > 1 and sys.argv[1] == "--historico":
    mostrar_historico()    # Mostra o histórico
    sys.exit(0)            # Encerra o programa


# ==================== ENTRADA DE DADOS ====================

# Tenta capturar peso e altura diretamente pela linha de comando
if len(sys.argv) == 3:
    try:
        peso = float(sys.argv[1])    # Converte primeiro argumento para número
        altura = float(sys.argv[2])  # Converte segundo argumento para número
    except ValueError:
        print("❌ Erro: Os valores devem ser números válidos.")
        print("Exemplo: python app.py 75 1.75")
        sys.exit(1)   # Encerra o programa com erro
else:
    # Modo interativo (pergunta ao usuário)
    print("Modo interativo:")
    
    # Loop para garantir que o peso seja válido
    while True:
        try:
            peso = float(input("Digite seu peso em kg (ex: 75): "))
            if peso <= 0:
                print("❌ O peso deve ser maior que zero.")
                continue
            break
        except ValueError:
            print("❌ Por favor, digite um número válido.")
    
    # Loop para garantir que a altura seja válida
    while True:
        try:
            altura = float(input("Digite sua altura em metros (ex: 1.75): "))
            if altura <= 0:
                print("❌ A altura deve ser maior que zero.")
                continue
            break
        except ValueError:
            print("❌ Por favor, digite um número válido.")


# ==================== EXECUÇÃO DO CÁLCULO ====================

try:
    # Chama a função de cálculo
    imc, classificacao, emoji = calcular_imc(peso, altura)
    
    # Exibe o resultado formatado
    print("\n" + "="*50)
    print(f"📊 Seu IMC é: {imc:.2f}")
    print(f"{emoji} Classificação: {classificacao}")
    print("="*50)
    
    # Calcula e mostra a faixa de peso ideal
    peso_ideal_min = 18.5 * (altura ** 2)
    peso_ideal_max = 24.9 * (altura ** 2)
    print(f"🔢 Peso ideal para sua altura: {peso_ideal_min:.1f}kg até {peso_ideal_max:.1f}kg")
    
    # Dica personalizada conforme o resultado
    if imc < 18.5:
        print("\n💡 Dica: Consulte um nutricionista para ganho de peso saudável.")
    elif imc < 25:
        print("\n🎉 Parabéns! Você está com o peso adequado.")
    else:
        print("\n💡 Dica: Pratique atividade física e consulte um profissional de saúde.")
    
    # Salva o cálculo no histórico
    salvar_historico(peso, altura, imc, classificacao)

except ValueError as erro:
    print(f"❌ Erro durante o cálculo: {erro}")


# Mensagem final de ajuda
print("\n📌 Dica: Use o comando abaixo para ver o histórico:")
print("   python app.py --historico")