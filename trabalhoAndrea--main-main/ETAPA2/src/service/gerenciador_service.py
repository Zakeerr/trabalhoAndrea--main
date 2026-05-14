from src.core.lista import ListaTarefas
from src.core.fila import FilaPendencias
from src.core.pilha import PilhaHistorico
from src.core.tarefa import Tarefa
from src.database.tarefa_repository import TarefaRepository

class GerenciadorService:
    def __init__(self):
        self.lista = ListaTarefas()
        self.fila = FilaPendencias()
        self.pilha = PilhaHistorico()
        self.repository = TarefaRepository()

    def cadastrar_tarefa(self, titulo, descricao, disciplina, prazo):
        tarefa = Tarefa(titulo, descricao, disciplina, prazo)

        self.lista.inserir(tarefa)
        self.fila.enqueue(tarefa)
        self.repository.salvar(tarefa)

        return tarefa

    def listar_tarefas(self):
        return self.lista.exibir()

    def buscar_tarefa(self, titulo):
        return self.lista.buscar(titulo)

    def proxima_tarefa(self):
        return self.fila.peek()

    def concluir_tarefa(self):
        tarefa = self.fila.dequeue()

        if tarefa is None:
            return None

        tarefa.concluir()

        self.pilha.push(tarefa)

        return tarefa

    def desfazer_ultima_acao(self):
        tarefa = self.pilha.pop()

        if tarefa is None:
            return None

        tarefa.restaurar()

        self.fila.enqueue(tarefa)

        return tarefa

    def excluir_tarefa(self, indice):
        return self.lista.remover(indice)

    def carregar_arquivo(self, caminho):
        try:
            with open(caminho, "r", encoding="utf-8") as arquivo:

                for linha in arquivo:
                    dados = linha.strip().split(";")

                    if len(dados) == 4:
                        titulo, descricao, disciplina, prazo = dados

                        self.cadastrar_tarefa(
                            titulo,
                            descricao,
                            disciplina,
                            prazo
                        )
                        
            return True

        except FileNotFoundError:
            return False