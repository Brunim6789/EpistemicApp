from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
import webbrowser
import os

#Vamos criar um arquivo de texto, para ajudar a simular o app, se ele ja n existir:
if not os.path.isfile("Dados_usuarios.txt"):
    with open("Dados_usuarios.txt", "w") as f:
        #Adicionando um usuario padrao (Separados por virgula:
        f.write("Bruno Vieira Ramos Silva,bruno.vrs@outlook.com,12345")




class LoginPage(GridLayout):
    def __init__(self, **kwargs):
        super(LoginPage, self).__init__(**kwargs)

        #Definindo uma variavel para contar a quantidade de erros de um usuario:
        self.contador_de_erros = 0

        #Email
        self.cols= 2
        self.add_widget(Label(text= "Email: "))
        self.email= TextInput(multiline= False)
        self.add_widget(self.email)

        #Senha
        self.add_widget(Label(text= "Senha: "))
        self.senha= TextInput(multiline= False)
        self.add_widget(self.senha)

        #Agora, a gente cria o botao de entrar, e associa ele a função de verificar o email:
        self.botaoEntrar = Button(text= "Entrar")
        self.botaoEntrar.bind(on_press=self.verificaLogin)
        self.add_widget(self.botaoEntrar)


        #Vamos agora adicionar os hyperlink.
        #Recuperacao de senha:
        self.textSenha = (Label(text="Esqueceu sua senha? [b][ref=Clique Aqui]Clique Aqui[/ref][/b]", markup=True))
        self.textSenha.on_ref_press = self.hyperSenha
        self.add_widget(self.textSenha)

        #Criar conta
        self.textConta = (Label(text="Não tem uma conta? [b][ref=Cadastre-se]Cadastre-se[/ref][/b]", markup=True))
        self.textConta.on_ref_press = self.hyperConta
        self.add_widget(self.textConta)

        #Termos de uso
        self.textTermos = (Label(text="[ref=Termos de uso]Termos de uso[/ref][/b]", markup=True))
        self.textTermos.on_ref_press = self.hyperTermos
        self.add_widget(self.textTermos)


    #Criando os direcionamento dos hyperlinks:
    def hyperConta(self, instance):
        aplication.screen_manager.current = "CriarAcc"

    def hyperSenha(self, instance):
        aplication.screen_manager.current = "Rec_Senha"

    def hyperTermos(self, instance):
        aplication.screen_manager.current = "Termos"


    #Criando a funcao que sobe o Popup para usuario invalido
    def show_popupUser(self):
        show = PopupInvalidUser()
        popupWindow = Popup(title= "Usuario nao existente", content= show, size_hint=(None, None))
        popupWindow.open()

    #Criando a funcao que sobe o Popup
    def show_popupBlocked(self):
        show = PopupUserBlocked()
        popupWindow = Popup(title= "Bloqueado", content= show, size_hint=(None, None), size=(400,400))
        popupWindow.open()


    def verificaLogin(self, instance):
        if (self.contador_de_erros >= 3):
            self.show_popupBlocked()

        else:
            email = self.email.text
            senha = self.senha.text

            #A gente começa por abrir o arquivo de texto que criamos, com o proposito de ajudar na simulacao:
            i=0
            with open("Dados_usuarios.txt", "r") as f:
                try:
                    Linha_Data = f.read().split(",")
                    while(True):
                        nome = Linha_Data[0+i]
                        email_Data = Linha_Data[1+i]
                        senha_Data = Linha_Data[2+i]

                        #Agora a gente compara as entradas:
                        if email == email_Data and senha == senha_Data:
                            #Entao ele logou com sucesso, portanto, ele vai para a pagina de usuario, e reseta o contador de erros.
                            self.contador_de_erros=0
                            aplication.screen_manager.current = "user"


                        i+=3
                except:
                    #Se não achar o usuario, e chegar ao fim do arquivo, mostrar o popup de usuario nao existente
                    if aplication.screen_manager.current != "user":
                        self.show_popupUser()
                    #acrescentar 1 ao valor de tentativas falhas
                    self.contador_de_erros += 1

        #Limpa a entrada
        self.senha.text=''



#Criando a tela de Popup para email ou senha invalida, qual será um float layout:
class PopupInvalidUser(FloatLayout):
    def __init__(self, **kwargs):
        super(PopupInvalidUser, self).__init__(**kwargs)
        self.cols=1

        self.mensagem = Label(text="Voce digitou o email ou senha incorretamente", pos_hint={"x":0, "top": 0.7})
        self.add_widget(self.mensagem)



#Criando a tela de Popup para dizer que o usuario foi bloqueado, por errar o login mais do que 3 vezes:
class PopupUserBlocked(FloatLayout):
    def __init__(self, **kwargs):
        super(PopupUserBlocked, self).__init__(**kwargs)
        self.cols=1

        self.mensagem = Label(text="Voce errou o login 3 vezes e foi bloqueado", pos_hint={"x":0, "top":0.75})
        self.add_widget(self.mensagem)


#Criando a pagina do usuario:
class UserPag(GridLayout):
    def __init__(self, **kwargs):
        super(UserPag, self).__init__(**kwargs)
        self.cols=1

        self.add_widget(Label(text="Bem vindo(a)"))

        #Adicionando o botão de retornar:
        self.botaoVoltar = Button(text= "Voltar", pos_hint={"x":0, "top": 1})
        self.botaoVoltar.bind(on_press=FinalApp.TelaLogin)
        self.add_widget(self.botaoVoltar)

#Criando a pagina de criaçao de conta:
class CriarConta(GridLayout):
    def __init__(self, **kwargs):
        super(CriarConta, self).__init__(**kwargs)


        self.cols= 2

        #Nome:
        self.add_widget(Label(text= "Nome: "))
        self.nome= TextInput(multiline= False)
        self.add_widget(self.nome)

        #Email
        self.add_widget(Label(text= "Email: "))
        self.email= TextInput(multiline= False)
        self.add_widget(self.email)

        #Senha
        self.add_widget(Label(text= "Defina sua Senha: "))
        self.senha= TextInput(multiline= False)
        self.add_widget(self.senha)

        #Agora, a gente cria o botao de entrar, e associa ele a funçao de verificar o email:
        self.botaoEntrar = Button(text= "Confirmar")
        self.botaoEntrar.bind(on_press=self.ConfereDados)
        self.add_widget(self.botaoEntrar)

        #Adicionando o botao de retornar:
        self.botaoVoltar = Button(text= "Voltar", pos_hint={"x":0, "top": 1})
        self.botaoVoltar.bind(on_press=FinalApp.TelaLogin)
        self.add_widget(self.botaoVoltar)


    def show_popupEmailExistente(self):
        show = PopupSenha()
        popupWindow = Popup(title="Email ja cadastrado.", content=show, size_hint=(None, None))
        popupWindow.open()


    def ConfereDados(self, instance):
        nome = self.nome.text
        email = self.email.text

        i = 0
        with open("Dados_usuarios.txt", "r") as f:
            try:
                Linha_Data = f.read().split(",")
                while (True):
                    self.nome_Data = Linha_Data[0 + i]
                    self.email_Data = Linha_Data[1 + i]
                    self.senha_Data = Linha_Data[2 + i]


                    # Agora a gente compara as entradas:
                    if email == self.email_Data:
                        # Entao existe o usuario em questao, e a senha e retornada com um popup
                        #print(self.senha_Data)
                        self.show_popupEmailExistente()
                        break

                    i += 3
            except:
                #Caso contrario, se chegar ate aqui, e porque nao existe o usuario em questao. Entao a gente grava ele
                self.GravaDados()

        #Limpa as caixas
        self.nome.text=''
        self.email.text=''



    def GravaDados(self):
        with open("Dados_usuarios.txt", "a") as f:
            f.write(','+self.nome.text+','+self.email.text+','+self.senha.text)

            #Limpa as caixas
            self.nome.text=''
            self.email.text=''
            self.senha.text=''

        #Retorna a tela de login:
        aplication.screen_manager.current= "LoginPage"
        pass

class TermosUsos(GridLayout):
    def __init__(self, **kwargs):
        super(TermosUsos, self).__init__(**kwargs)

        self.cols= 1

        #Texto com hyperlink para o site da epistemic
        self.textTermos = (Label(text="Aqui encontra-se um exemplo de Termos\nde uso do aplicativo."
                                   "\nPara mais detalhes, visite:[b][ref=Epistemic.com.br]Epistemic.com.br[/ref][/b]", markup=True))
        self.textTermos.on_ref_press = self.linkEpistemic
        self.add_widget(self.textTermos)


        #Adicionando o botão de retornar:
        self.botaoVoltar = Button(text= "Voltar", pos_hint={"x":0, "top": 1})
        self.botaoVoltar.bind(on_press=FinalApp.TelaLogin)
        self.add_widget(self.botaoVoltar)

    #Função que leva ao site da epistemic.
    def linkEpistemic(self, instance):
        webbrowser.open("https://epistemic.com.br/#/")




#Tela para recuperação de senha. Pede o Nome e o Email, e retorna a senha como um popup
class RecSenha(GridLayout):
    def __init__(self, **kwargs):
        super(RecSenha, self).__init__(**kwargs)
        self.cols= 2

        #Nome
        self.add_widget(Label(text= "Nome: "))
        self.nome= TextInput(multiline= False)
        self.add_widget(self.nome)

        #Senha
        self.add_widget(Label(text= "Email: "))
        self.email= TextInput(multiline= False)
        self.add_widget(self.email)


        #Adicionando o botao de enviar:
        self.botaoEnviar = Button(text= "Enviar", pos_hint={"x":0, "top": 1})
        self.botaoEnviar.bind(on_press=self.RetrievePass)
        self.add_widget(self.botaoEnviar)


        #Adicionando o botao de retornar:
        self.botaoVoltar = Button(text= "Voltar", pos_hint={"x":0, "top": 1})
        self.botaoVoltar.bind(on_press=FinalApp.TelaLogin)
        self.add_widget(self.botaoVoltar)


    # Criando a funçao que sobe o Popup com a senha do usuario
    def show_popupSenha(self):
        show = PopupSenha()
        popupWindow = Popup(title="Sua senha: "+self.senha_Data, content=show, size_hint=(None, None))
        popupWindow.open()

    # Criando a funçao que sobe o Popup para usuario invalido
    def show_popupUsuarioInexistente(self):
        show = PopupUsuarioInexistente()
        popupWindow = Popup(title="", content=show, size_hint=(None, None))
        popupWindow.open()


    def RetrievePass(self, instance):
        nome = self.nome.text
        email = self.email.text

        i = 0
        with open("Dados_usuarios.txt", "r") as f:
            try:
                Linha_Data = f.read().split(",")
                while (True):
                    self.nome_Data = Linha_Data[0 + i]
                    self.email_Data = Linha_Data[1 + i]
                    self.senha_Data = Linha_Data[2 + i]


                    # Agora a gente compara as entradas:
                    if email == self.email_Data and nome == self.nome_Data:
                        # Entao existe o usuario em questao, e a senha e retornada com um popup
                        #print(self.senha_Data)
                        self.show_popupSenha()
                        break

                    i += 3
            except:
                #Caso contrario, se chegar ate aqui, e porque nao existe o usuario em questao. Retorna um popup.
                self.show_popupUsuarioInexistente()

        #Limpa as caixas
        self.nome.text=''
        self.email.text=''


class PopupSenha(FloatLayout):
    def __init__(self, **kwargs):
        super(PopupSenha, self).__init__(**kwargs)
        self.cols=1

        self.mensagem = Label(text="", pos_hint={"x":0, "top": 0.7})
        self.add_widget(self.mensagem)

class PopupUsuarioInexistente(FloatLayout):
    def __init__(self, **kwargs):
        super(PopupUsuarioInexistente, self).__init__(**kwargs)
        self.cols=1

        self.mensagem = Label(text="Usuario Inexistente", pos_hint={"x":0, "top": 0.7})
        self.add_widget(self.mensagem)


class FinalApp(App):
    def TelaLogin(self):
        aplication.screen_manager.current="LoginPage"



    def build(self):
        #referenciando o objeto manager
        self.screen_manager = ScreenManager()

        #Fazendo com q a Login page seja vista como uma screen
        self.login_page = LoginPage()
        screen = Screen(name="LoginPage")
        screen.add_widget(self.login_page)
        #Agora, a gente atribui esta screen adicionada ao manager, como parent
        self.screen_manager.add_widget(screen)

        #Seguindo o mesmo padrao, vamos fazer agora 3 telas que serao ativadas por hiperlink
        # Recuperar senha:
        self.rec_senha = RecSenha()
        screen = Screen(name="Rec_Senha")
        screen.add_widget(self.rec_senha)
        self.screen_manager.add_widget(screen)

        #Criar conta:
        self.criar_conta = CriarConta()
        screen = Screen(name="CriarAcc")
        screen.add_widget(self.criar_conta)
        self.screen_manager.add_widget(screen)

        #Termos e usos:
        self.termos_usos = TermosUsos()
        screen = Screen(name="Termos")
        screen.add_widget(self.termos_usos)
        self.screen_manager.add_widget(screen)

        #Tela do usuario:
        self.usuario = UserPag()
        screen = Screen(name="user")
        screen.add_widget(self.usuario)
        self.screen_manager.add_widget(screen)


        return self.screen_manager


if __name__ == "__main__":
    aplication = FinalApp()
    aplication.run()
