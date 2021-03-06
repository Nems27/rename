from tkinter import *
from rules.rule import Rule

from rename.apply import Apply
from rename.action import Action
from interfaces.liste import LoadInterface
from interfaces.Sauve import SaveInterface

from utils.animatedgif import *
from utils.browser import Browser
from utils.tabulate import tabulate



class RenameInterface:

    def __init__(self, app):
        self.app = app
        self.simulation = False
        self.params = {
            'init': None,
            'beginwith': None,
            'prefix': None,
            'suffix': None,
            'original': None,
            'extension': None,
            'dirname': None,
            'rulename' : None
        }

    def tkTemp(self):
        root = Tk()
        root.eval('tk::PlaceWindow %s center' % root.winfo_pathname(root.winfo_id()))
        root.geometry("1024x512+300+100")
        root.title(self.app)


        self.set('init', StringVar())
        self.set('dirname', StringVar())
        self.set('prefix', StringVar())
        self.set('suffix', StringVar())
        self.set('original', StringVar())
        self.set('beginwith', StringVar())
        self.set('extension', StringVar())
        self.set('rulename', StringVar())

        # List | Create
        Button(root, text="Lister", command = lambda: self.load()).grid(row = 0, column = 0, stick = W)
        Button(root, text="Créer", command = lambda: self.save(self.params)).grid(row = 1, column = 0, stick = W)

        # Directory name
        Label(root, text="Renommer en lots").grid(row=1, column=2)
        Label(root, text = "Nom du répertoire").grid(row = 2, column = 1)
        Entry(root, textvariable = self.get('dirname')).grid(row = 2, column = 2, stick = W)
        Button(root, text = "Choisir un chemin", command = lambda: self.setPath()).grid(row = 2, column = 3, stick = W)

        # Init
        Label(root, text = "Amorce").grid(row = 4, column = 0, stick = W)
        Button(root, text = "Aucune", command = lambda: self.get('init').set(None)).grid(row = 5, column = 0, stick = W)
        Button(root, text = "Lettre", command = lambda: self.get('init').set('letter')).grid(row = 6, column = 0, stick = W)
        Button(root, text = "Chiffre", command = lambda: self.get('init').set('chiffre')).grid(row = 7, column = 0, stick = W)

        # Begin with
        Label(root, text = "A partir de").grid(row = 8, column = 0, stick = W)
        Entry(root, textvariable = self.get('beginwith')).grid(row = 9, column = 0,stick = W)

        # Prefix
        Label(root, text = "Préfixe").grid(row = 4, column = 1)
        Entry(root, textvariable = self.get('prefix')).grid(row = 5, column = 1)

        #Original name or not
        Label(root, text = "Nom original").grid(row = 5, column = 2)
        Label(root, text="Nouveau nom").grid(row=6, column=2)
        Entry(root, textvariable=self.get('original')).grid(row=7, column=2)

        # Suffix
        Label(root, text = "Postfixe").grid(row = 4, column = 3)
        Entry(root, textvariable = self.get('suffix')).grid(row = 5, column = 3)

        #Extension
        Label(root, text = "Extension concernée").grid(row = 4, column = 4)
        Entry(root, textvariable = self.get('extension')).grid(row = 5, column = 4)

        # Rename button
        Button(root, text = "Renommer", command = lambda : self.rename()).grid(row = 7, column = 4)

        # Image
        img = AnimatedGif(root, 'yes.gif', 0.05)
        img.place(x = 650, y = 0)
        img.start()

        #Simulate
        Checkbutton(root, text="Simuler", command = lambda: self.simulate()).grid(row = 9, column = 1)
        root.mainloop()

    def setPath(self):
        """
        Define current path with Windows Browser
        """
        file = Browser()
        self.get('dirname').set(file.get())

    def simulate(self):
        """
        Enable / disable simulation mode
        """
        self.simulation = not self.simulation

    def set(self, option, value):
        """
        Set a value (object)
        """
        self.params[option] = value

    def save(self, params):
        """
        Open the save GUI
        """
        rule = Rule(self.params['init'].get(), self.params['beginwith'].get(),
                    self.params['prefix'].get(), self.params['dirname'].get(),
                    self.params['suffix'].get(), self.params['extension'].get(),
                    self.params['original'].get())

        save = SaveInterface(rule)
        save.tkSave()


    def load(self):
        """
        Open the load GUI
        """
        load = LoadInterface(self);
        load.tkList();

    def get(self, option):
        """
        Get a value (object)
        """
        return self.params[option]

    def rename(self):
        init = (self.get('init').get(), None)[self.get('init').get() == ""]
        extension = ([x.strip() for x in self.get('extension').get().split(',')], None)[self.get('extension').get() == ""]
        beginwith = self.get('beginwith').get()
        prefix = self.get('prefix').get()
        suffix = self.get('suffix').get()
        original = self.get('original').get()
        dirname = self.get('dirname').get()

        if beginwith == "": beginwith = ("001", "A")[init == "letter"]

        # Rule & Util
        rule = Rule(init, beginwith, prefix, dirname, suffix, original, extension)


        if (self.simulation):
            action = Action(self.get('dirname').get(), rule)

            # Simulation
            header = ["Fichier original", "Renommé"]
            final = action.arrayEdit()

            # Debug
            print("")
            print(tabulate(final, header, tablefmt="simple"))

            return

        rename = Apply(self.get('dirname').get(), rule)
        rename.applyRename()
