from jupyter_server.services.contents.manager import ContentsManager

# Abstract ContentsManager, should disable all contents
c.ServerApp.contents_manager_class = ContentsManager

c.ServerApp.allow_unauthenticated_access = False

