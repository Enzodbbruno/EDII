import math
from typing import List, Optional, Tuple

class NoBPlus:
    def __init__(self, t: int, folha: bool):
        self.t = t 
        self.folha = folha 
        self.chaves: List[int] = [] 
        self.filhos: List['NoBPlus'] = [] 
        self.proximo_irmao: Optional['NoBPlus'] = None 

    def __len__(self):
        return len(self.chaves)
    
    def is_full(self) -> bool:
        return len(self.chaves) == 2 * self.t - 1

class ArvoreBPlus:
    def __init__(self, t: int):
        self.t = t 
        self.raiz: Optional[NoBPlus] = None
        self.historico: List[str] = []

        if self.t < 2:
            raise ValueError("A ordem mínima (t) deve ser 2 ou maior.")
        
        self.criar_arvore()
        self.historico.append(f"Árvore B+ de ordem mínima (t)={t} criada.")

    def criar_arvore(self):
        self.raiz = NoBPlus(self.t, folha=True)
        self.historico.append("Árvore B+ inicializada com nó raiz vazio.")

    def _encontrar_caminho_e_folha(self, chave: int) -> Tuple[List[NoBPlus], Optional[NoBPlus]]:
        caminho = []
        atual = self.raiz
        if not atual: 
            return caminho, None

        while not atual.folha:
            caminho.append(atual)
            i = 0
            while i < len(atual) and chave >= atual.chaves[i]:
                i += 1
            atual = atual.filhos[i]
        return caminho, atual

    
    def inserir(self, chave: int):
        self.historico.append(f"Operação: Inserir chave {chave}")
        
        caminho, folha = self._encontrar_caminho_e_folha(chave)
        
        if not folha:
            self.historico.append("  -> Árvore vazia após inicialização. Não deve ocorrer.")
            return
        
        i = 0
        while i < len(folha) and chave > folha.chaves[i]:
            i += 1
        
        if i < len(folha) and chave == folha.chaves[i]:
            self.historico.append(f"  -> Chave {chave} já existe (ignorado).")
            print(f"Chave {chave} já existe na folha.")
            return
            
        folha.chaves.insert(i, chave)
        self.historico.append(f"  -> Chave {chave} inserida na folha {folha.chaves}.")

        if folha.is_full():
            self._split_folha(folha, caminho)
            
        self.historico.append(f"Inserção de {chave} finalizada.")

    def _split_folha(self, y: NoBPlus, caminho: List[NoBPlus]):
        self.historico.append(f"  -> SPLIT FOLHA: Nó {y.chaves} cheio. Divisão necessária.")
        
        z = NoBPlus(self.t, folha=True)
        
        mediana_index = self.t 
        
        z.chaves = y.chaves[mediana_index:]
        
        y.chaves = y.chaves[:mediana_index]
        
        z.proximo_irmao = y.proximo_irmao
        y.proximo_irmao = z
        
        chave_a_subir = z.chaves[0]
        
        self._propagacao_de_indice(caminho, chave_a_subir, y, z)

        self.historico.append(f"  -> SPLIT FOLHA: Chave de índice {chave_a_subir} copiada para o índice. Folha Z: {z.chaves}.")

    def _propagacao_de_indice(self, caminho: List[NoBPlus], chave: int, filho_esq: NoBPlus, filho_dir: NoBPlus):
        
        if not caminho:
            nova_raiz = NoBPlus(self.t, folha=False)
            nova_raiz.chaves = [chave]
            nova_raiz.filhos = [filho_esq, filho_dir]
            self.raiz = nova_raiz
            self.historico.append(f"  -> NOVA RAIZ criada com índice {chave}.")
            return

        pai = caminho.pop()
        
        i = 0
        while i < len(pai) and chave > pai.chaves[i]:
            i += 1
            
        pai.chaves.insert(i, chave)
        pai.filhos.insert(i + 1, filho_dir)
        
        self.historico.append(f"  -> Índice {chave} inserido no nó interno: {pai.chaves}.")

        if pai.is_full():
            chave_promovida, novo_irmao = self._split_interno(pai)
            self._propagacao_de_indice(caminho, chave_promovida, pai, novo_irmao)

    def _split_interno(self, y: NoBPlus) -> Tuple[int, NoBPlus]:
        self.historico.append(f"  -> SPLIT INTERNO: Nó índice {y.chaves} cheio. Divisão necessária.")
        
        z = NoBPlus(self.t, folha=False)
        
        mediana_index = self.t - 1
        chave_a_subir = y.chaves[mediana_index]
        
        z.chaves = y.chaves[self.t:]
        
        z.filhos = y.filhos[self.t:]
        
        y.chaves = y.chaves[:mediana_index]
        y.filhos = y.filhos[:self.t]

        self.historico.append(f"  -> SPLIT INTERNO: Chave {chave_a_subir} promovida. Novo nó Z: {z.chaves}.")

        return chave_a_subir, z

    
    def excluir(self, chave: int):
        self.historico.append(f"Operação: Excluir chave {chave}")

        caminho, folha = self._encontrar_caminho_e_folha(chave)
        
        if not folha:
            self.historico.append("  -> Árvore vazia. Exclusão não realizada.")
            print("Árvore vazia.")
            return

        if chave in folha.chaves:
            folha.chaves.remove(chave)
            self.historico.append(f"  -> Chave {chave} removida da folha.")
            
            print(f"Chave {chave} removida. Lógica de rebalanceamento (fusão/redistribuição) não implementada.")
            
        else:
            print(f"Chave {chave} não encontrada.")
            self.historico.append(f"  -> Chave {chave} não encontrada.")


    
    def exibir_arvore(self):
        if not self.raiz or (len(self.raiz.chaves) == 0 and self.raiz.folha):
            print("\n--- Árvore B+ VAZIA ---")
            return
        
        max_chaves = 2 * self.t - 1
        min_chaves = self.t - 1
        print(f"\n--- Estrutura da Árvore B+ (t={self.t}, Mín Chaves={min_chaves}, Máx Chaves={max_chaves}) ---")
        self._exibir_recursivo(self.raiz, 0)
        
        self._exibir_encadeamento_folhas()
        
        print("------------------------------------------")

    def _exibir_recursivo(self, no: NoBPlus, nivel: int):
        indentacao = "  | " * nivel
        
        status = "(FOLHA/DADOS)" if no.folha else "(INTERNO/ÍNDICE)"
        chaves_str = ", ".join(map(str, no.chaves))
        print(f"{indentacao}Nível {nivel} {status} [{chaves_str}]")
        
        if not no.folha:
            for i, filho in enumerate(no.filhos):
                self._exibir_recursivo(filho, nivel + 1)
                
    def _exibir_encadeamento_folhas(self):
        
        primeira_folha = self.raiz
        if not primeira_folha:
            return

        while not primeira_folha.folha:
            if not primeira_folha.filhos:
                break # Evita erro em caso de estrutura malformada, embora não deva acontecer
            primeira_folha = primeira_folha.filhos[0]
            
        print("\n--- Encadeamento Sequencial das Folhas ---")
        folhas_encadeadas = []
        atual = primeira_folha
        
        while atual:
            folhas_encadeadas.append(f"[{', '.join(map(str, atual.chaves))}]")
            atual = atual.proximo_irmao
            
        print(" -> ".join(folhas_encadeadas))
        print("------------------------------------------")

    
    def verificar_historico(self):
        if not self.historico:
            print("\nNenhuma operação registrada ainda.")
            return

        print("\n--- Histórico de Operações da Árvore B+ ---")
        for i, op in enumerate(self.historico, 1):
            print(f"{i:03d}: {op}")
        print("------------------------------------------")


def menu_interativo():
    
    while True:
        try:
            t = int(input("Defina a Ordem Mínima (t) da Árvore B+ (ex: 3, 4, 5...): "))
            if t < 2:
                print("A ordem mínima (t) deve ser 2 ou maior.")
            else:
                arvore_bplus = ArvoreBPlus(t)
                break
        except ValueError:
            print("Entrada inválida. Por favor, digite um número inteiro.")

    while True:
        print("\n===============================")
        print("       Menu Árvore B+        ")
        print(f"      (Ordem Mínima t={t})     ")
        print("===============================")
        print("1. Criar/Inserir nó")
        print("2. Excluir nó (Implementação parcial)")
        print("3. Exibir a estrutura da árvore")
        print("4. Verificar histórico de operações")
        print("5. Sair")
        print("===============================")

        try:
            opcao = input("Escolha uma opção: ")
            
            if opcao == '1':
                valor = int(input("Digite o valor (chave) para inserir: "))
                arvore_bplus.inserir(valor)
            elif opcao == '2':
                valor = int(input("Digite o valor (chave) para excluir: "))
                arvore_bplus.excluir(valor)
            elif opcao == '3':
                arvore_bplus.exibir_arvore()
            elif opcao == '4':
                arvore_bplus.verificar_historico()
            elif opcao == '5':
                print("Saindo do programa. Até mais!")
                break
            else:
                print("Opção inválida. Tente novamente.")
        except ValueError:
            print("Erro: Entrada inválida. Por favor, digite um número inteiro.")
        except Exception as e:
            print(f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    menu_interativo()