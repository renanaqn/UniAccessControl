import reflex as rx

# top 1 senhas
ADMIN_USER = "admin"
ADMIN_PASS = "admin"

class AuthState(rx.State):
    """Gerencia a sessão de login do sistema"""
    
    is_authenticated: bool = False
    
    login_user: str = ""
    login_pass: str = ""
    erro_login: str = ""

    def set_login_user(self, v: str): self.login_user = v
    def set_login_pass(self, v: str): self.login_pass = v

    def verificar_acesso(self):
        """Guarda-costas: roda no on_load da página para barrar intrusos"""
        if not self.is_authenticated:
            return rx.redirect("/")

    def fazer_login(self):
        """Verifica se o usuário e senha batem"""
        if self.login_user == ADMIN_USER and self.login_pass == ADMIN_PASS:
            self.is_authenticated = True
            self.erro_login = ""
            self.login_user = "" 
            self.login_pass = ""
            
            return rx.redirect("/dashboard")
        else:
            self.erro_login = "Acesso Negado: Usuário ou senha incorretos."

    def fazer_logout(self):
        """Encerra a sessão e vai para a tela inicial"""
        self.is_authenticated = False
        return rx.redirect("/")
    
