import math
from typing import List, Optional, Tuple

class NoB:
    def __init__(self, t: int, folha: bool):
        self.t = t
        self.folha = folha
        self.chaves: List[str] = []
        self.filhos: List['NoB'] = []

    def __len__(self):
        return len(self.chaves)
    
    def is_full(self) -> bool:
        return len(self.chaves) == 2 * self.t - 1

class ArvoreB:
    def __init__(self, t: int):
        self.t = t
        self.raiz: Optional[NoB] = None
        self.historico: List[str] = []

        if self.t < 2:
            raise ValueError("A ordem mínima (t) deve ser 2 ou maior.")
        
        self.criar_arvore()
        self.historico.append(f"Árvore B de ordem mínima (t)={t} (Chaves: Letras) criada.")

    def criar_arvore(self):
        self.raiz = NoB(self.t, folha=True)
        self.historico.append("Árvore inicializada com nó raiz vazio.")

    def _min_chaves(self) -> int:
        return self.t - 1
    
    def _is_min(self, no: NoB) -> bool:
        if no is self.raiz:
            return len(no) == 0 and not no.folha
        return len(no) < self._min_chaves()
    
    def inserir(self, chave: str):
        chave = chave.upper()
        self.historico.append(f"Operação: Inserir chave '{chave}'")
        
        if self.raiz.is_full():
            s = NoB(self.t, folha=False)
            s.filhos.append(self.raiz)
            self.raiz = s
            self.historico.append(f"  -> Raiz cheia. Nova raiz criada para Split do Nó Antigo.")
            
            self._split_filho(s, 0, s.filhos[0])
            self._inserir_nao_cheio(s, chave)
        else:
            self._inserir_nao_cheio(self.raiz, chave)
        
        self.historico.append(f"Inserção de '{chave}' finalizada.")

    def _inserir_nao_cheio(self, no: NoB, chave: str):
        i = len(no) - 1
        
        if no.folha:
            if chave in no.chaves:
                self.historico.append(f"  -> Chave '{chave}' já existe (Não inserida).")
                print(f"Chave '{chave}' já existe na árvore.")
                return

            no.chaves.append('')
            while i >= 0 and chave < no.chaves[i]:
                no.chaves[i+1] = no.chaves[i]
                i -= 1
            no.chaves[i+1] = chave
            self.historico.append(f"  -> Chave '{chave}' inserida na folha.")
        else:
            while i >= 0 and chave < no.chaves[i]:
                i -= 1
            i += 1
            
            filho = no.filhos[i]
            if filho.is_full():
                self._split_filho(no, i, filho)
                if chave > no.chaves[i]:
                    i += 1
                
            self._inserir_nao_cheio(no.filhos[i], chave)

    def _split_filho(self, pai: NoB, i: int, y: NoB):
        self.historico.append(f"  -> SPLIT: Nó {y.chaves} cheio. Divisão necessária.")
        
        z = NoB(self.t, folha=y.folha)
        
        chave_a_subir = y.chaves[self.t - 1]
        
        z.chaves = y.chaves[self.t:]
        y.chaves = y.chaves[:self.t - 1]
        
        if not y.folha:
            z.filhos = y.filhos[self.t:]
            y.filhos = y.filhos[:self.t]

        pai.filhos.insert(i + 1, z)
        pai.chaves.insert(i, chave_a_subir)
        
        self.historico.append(f"  -> SPLIT: Chave '{chave_a_subir}' subiu (e foi removida do filho). Novo nó Z: {z.chaves}.")

    def excluir(self, chave: str):
        chave = chave.upper()
        self.historico.append(f"Operação: Excluir chave '{chave}'")
        
        if not self.raiz or (len(self.raiz.chaves) == 0 and self.raiz.folha):
            self.historico.append("  -> Árvore vazia. Exclusão não realizada.")
            print("Árvore vazia.")
            return

        self._excluir_chave(self.raiz, chave)
        
        if len(self.raiz) == 0 and not self.raiz.folha:
            if self.raiz.filhos:
                self.raiz = self.raiz.filhos[0]
                self.historico.append("  -> Raiz esvaziou após exclusão. Novo filho se torna a raiz.")
            else:
                self.raiz = NoB(self.t, folha=True)
                self.historico.append("  -> Árvore vazia.")

    def _excluir_chave(self, no: NoB, chave: str):
        i = 0
        while i < len(no) and chave > no.chaves[i]:
            i += 1
        
        if i < len(no) and chave == no.chaves[i]:
            
            if no.folha:
                no.chaves.pop(i)
                self.historico.append(f"  -> Chave '{chave}' removida da folha.")
                if self._is_min(no):
                    print(f"AVISO: Underflow na folha {no.chaves}. Lógica de rebalanceamento (fusão/redistribuição) não implementada.")
                    self.historico.append(f"  -> WARNING: Underflow na folha. Lógica de rebalanceamento pendente.")
                
            else:
                print(f"AVISO: Chave '{chave}' encontrada em nó interno. A lógica de substituição pelo antecessor/sucessor e rebalanceamento subsequente não está implementada nesta versão.")
                self.historico.append(f"  -> WARNING: Chave '{chave}' (Nó Interno) encontrada. Deletar em nó interno não suportado nesta versão.")
            
            return

        if no.folha:
            print(f"Chave '{chave}' não encontrada.")
            self.historico.append(f"  -> Chave '{chave}' não encontrada.")
            return
        
        filho = no.filhos[i]
        
        if self._is_min(filho):
            print(f"AVISO: Nó filho {filho.chaves} tem underflow antes da descida. Lógica de redistribuição/fusão não implementada.")
            self.historico.append(f"  -> WARNING: Underflow no filho. Rebalanceamento (fusão/redistribuição) pendente.")
            
        self._excluir_chave(filho, chave)

    def _buscar_simples(self, no: NoB, chave: str):
        i = 0
        while i < len(no) and chave > no.chaves[i]:
            i += 1
        
        if i < len(no) and chave == no.chaves[i]:
            return no, i
        
        if no.folha:
            return None, -1
        
        return self._buscar_simples(no.filhos[i], chave)
            
    def exibir_arvore(self):
        if not self.raiz or (len(self.raiz.chaves) == 0 and self.raiz.folha):
            print("\n--- Árvore B VAZIA ---")
            return
        
        min_chaves = self._min_chaves()
        max_chaves = 2 * self.t - 1
        print(f"\n--- Estrutura da Árvore B (t={self.t}, Mín Chaves={min_chaves}, Máx Chaves={max_chaves}) ---")
        self._exibir_recursivo(self.raiz, 0)
        print("------------------------------------------")

    def _exibir_recursivo(self, no: NoB, nivel: int):
        indentacao = "  | " * nivel
        status = "(FOLHA/DADOS)" if no.folha else "(INTERNO/DADOS)"
        chaves_str = ", ".join(no.chaves)
        print(f"{indentacao}Nível {nivel} {status} ['{chaves_str}']")
        
        if not no.folha:
            for i, filho in enumerate(no.filhos):
                self._exibir_recursivo(filho, nivel + 1)
                
    def verificar_historico(self):
        if not self.historico:
            print("\nNenhuma operação registrada ainda.")
            return

        print("\n--- Histórico de Operações da Árvore B ---")
        for i, op in enumerate(self.historico, 1):
            print(f"{i:03d}: {op}")
        print("------------------------------------------")


def menu_interativo():
    while True:
        try:
            t = int(input("Defina a Ordem Mínima (t) da Árvore B (ex: 3, 4, 5...): "))
            if t < 2:
                print("A ordem mínima (t) deve ser 2 ou maior.")
            else:
                arvore_b = ArvoreB(t)
                break
        except ValueError:
            print("Entrada inválida. Por favor, digite um número inteiro.")

    while True:
        print("\n===============================")
        print("        Menu Árvore B        ")
        print(f"      (Ordem Mínima t={t})     ")
        print("      Chaves: LETRAS/TEXTO    ")
        print("===============================")
        print("1. Inserir chave(s) (separadas por vírgula)")
        print("2. Excluir chave (Implementação parcial)")
        print("3. Exibir a estrutura da árvore")
        print("4. Verificar histórico de operações")
        print("5. Sair")
        print("===============================")

        try:
            opcao = input("Escolha uma opção: ")
            
            if opcao == '1':
                valores_input = input("Digite as chaves (letras/texto) para inserir, separadas por vírgula (ex: A, B, C): ")
                
                if not valores_input:
                    print("A chave não pode ser vazia.")
                    continue
                    
                chaves = [v.strip() for v in valores_input.split(',') if v.strip()]
                
                for chave in chaves:
                    arvore_b.inserir(chave)
                    
            elif opcao == '2':
                valor = input("Digite a chave (letra/texto) para excluir: ")
                if not valor:
                    print("A chave não pode ser vazia.")
                    continue
                arvore_b.excluir(valor.strip())
            elif opcao == '3':
                arvore_b.exibir_arvore()
            elif opcao == '4':
                arvore_b.verificar_historico()
            elif opcao == '5':
                print("Saindo do programa. Até mais!")
                break
            else:
                print("Opção inválida. Tente novamente.")
        except Exception as e:
            print(f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    menu_interativo()
