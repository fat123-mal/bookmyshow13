from django.core.mail.backends.smtp import EmailBackend as DjangoEmailBackend

class PatchedEmailBackend(DjangoEmailBackend):
    def open(self):
        if self.connection:
            return False

        connection_params = {}
        self.connection = self.connection_class(self.host, self.port, **connection_params)

        if self.use_tls:
            self.connection.starttls()

        if self.username and self.password:
            self.connection.login(self.username, self.password)

        return True
