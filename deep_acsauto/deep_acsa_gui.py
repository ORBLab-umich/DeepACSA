from tkinter import StringVar, Tk, tkk, filedialog, N, S, W, E
from tkinter.tix import *
from PIL import Image, ImageTk
from predict_muscle_area import calculate_batch, calculate_batch_efov


class DeepACSA:
    def __init__(self, root):

        root.title("DeepACSA")
        root.iconbitmap("icon.ico")

        main = ttk.Frame(root, padding="10 10 12 12")
        main.grid(column=0, row=0, sticky=(N, S, W, E))
        # Configure resizing of user interface
        main.columnconfigure(0, weight=1)
        main.columnconfigure(1, weight=1)
        main.columnconfigure(2, weight=1)
        main.columnconfigure(3, weight=1)
        main.columnconfigure(4, weight=1)
        main.columnconfigure(5, weight=1)
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        # Tooltips
        tip = Balloon(root)

        # Paths
        # Input directory
        self.input = StringVar()
        input_entry = ttk.Entry(main, width=30, textvariable=self.input)
        input_entry.grid(column=2, row=1, columnspan=3, sticky=(W, E))
        # Model path
        self.model = StringVar()
        model_entry = ttk.Entry(main, width=30, textvariable=self.model)
        model_entry.grid(column=2, row=2, columnspan=3, sticky=(W, E))
        # Flag path
        self.flags = StringVar()
        flags_entry = ttk.Entry(main, width=14, textvariable=self.flags)
        flags_entry.grid(column=2, row=3, columnspan=3, sticky=(W, E))

        # Radiobuttons
        # Image Type
        self.scaling = StringVar()
        efov = ttk.Radiobutton(main, text="EFOV", variable=self.scaling,
                               value="EFOV")
        efov.grid(column=2, row=4, sticky=W)
        static = ttk.Radiobutton(main, text="Static", variable=self.scaling,
                                 value="Static")
        static.grid(column=3, row=4, sticky=(W, E))
        manual = ttk.Radiobutton(main, text="Manual", variable=self.scaling,
                                 value="Manual")
        manual.grid(column=4, row=4, sticky=E)
        tip.bind_widget(efov,
                        balloonmsg="Choose image type from dropdown list." +
                        " If image taken in panoramic mode, choose EFOV." +
                        " If image taken in static B-mode, choose Static." +
                        " If image taken in other modality, choose Manual" +
                        " in order to scale the image manually.")
        # Comboboxes
        # Muscles
        self.muscle = StringVar()
        muscle = ("VL", "RF", "GM", "GL")
        muscle_entry = ttk.Combobox(main, width=10, textvariable=self.muscle)
        muscle_entry["values"] = muscle
        muscle_entry["state"] = "readonly"
        muscle_entry.grid(column=2, row=6, sticky=(W, E))
        tip.bind_widget(muscle_entry,
                        balloonmsg="Choose muscle from dropdown list, " +
                        "depending on which muscle is analyzed.")
        # Image Depth
        self.depth = StringVar()
        depth = (2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7)
        depth_entry = ttk.Combobox(main, width=10, textvariable=self.depth)
        depth_entry["values"] = depth
        depth_entry["state"] = "readonly"
        depth_entry.grid(column=2, row=7, sticky=(W, E))
        tip.bind_widget(depth_entry,
                        balloonmsg="Choose image depth from dropdown list. " +
                        "Analyzed images must have the same depth.")
        # Spacing
        self.spacing = StringVar()
        spacing = (5, 10, 15, 20)
        spacing_entry = ttk.Combobox(main, width=10, textvariable=self.spacing)
        spacing_entry["values"] = spacing
        spacing_entry["state"] = "readonly"
        spacing_entry.grid(column=2, row=8, sticky=(W, E))
        tip.bind_widget(spacing_entry,
                        balloonmsg="Choose disance between scaling bars" +
                                   " in image form dropdown list. " +
                                   "Distance needs to be similar " +
                                   "in all analyzed images.")

        # Buttons
        # Input directory
        input_button = ttk.Button(main, text="Input",
                                  command=self.get_root_dir)
        input_button.grid(column=5, row=1, sticky=E)
        tip.bind_widget(input_button,
                        balloonmsg="Choose root directory." +
                        " This is the folder containing all images.")
        # Model path
        model_button = ttk.Button(main, text="Model",
                                  command=self.get_model_path)
        model_button.grid(column=5, row=2, sticky=E)
        tip.bind_widget(model_button,
                        balloonmsg="Choose model path." +
                        " This is the path to the respective model.")
        # Flip Flag path
        flags_button = ttk.Button(main, text="Flip Flag",
                                  command=self.get_flag_dir)
        flags_button.grid(column=5, row=3, sticky=E)
        tip.bind_widget(flags_button,
                        balloonmsg="Choose Flag File Path." +
                        " This is the path to the .txt file containing" +
                        " flipping info.")
        # Break Button
        break_button = ttk.Button(main, text="Break", command=self.do_break)
        break_button.grid(column=1, row=9, sticky=W)
        # Run Button
        run_button = ttk.Button(main, text="Run", command=self.run_code)
        run_button.grid(column=2, row=9, sticky=(W, E))

        # Labels
        ttk.Label(main, text="Root Directory").grid(column=1, row=1, sticky=W)
        ttk.Label(main, text="Model Path").grid(column=1, row=2, sticky=W)
        ttk.Label(main, text="Flip Flag Path").grid(column=1, row=3, sticky=W)
        ttk.Label(main, text="Image Type").grid(column=1, row=4, sticky=W)
        ttk.Label(main, text="Muscle").grid(column=1, row=6, sticky=W)
        ttk.Label(main, text="Depth (cm)").grid(column=1, row=7, sticky=W)
        ttk.Label(main, text="Spacing (mm)").grid(column=1, row=8, sticky=W)

        for child in main.winfo_children():
            child.grid_configure(padx=5, pady=5)

        # depth_entry.focus()
        root.bind("<Return>", self.run_code)  # execute by pressing return

    def get_root_dir(self):

        root_dir = filedialog.askdirectory()
        self.input.set(root_dir)
        return root_dir

    def get_model_path(self):

        model_dir = filedialog.askopenfilename()
        self.model.set(model_dir)
        return model_dir

    def get_flag_dir(self):

        flag_dir = filedialog.askopenfilename()
        self.flags.set(flag_dir)
        return flag_dir

    def run_code(self):

        selected_muscle = self.muscle.get()
        selected_depth = float(self.depth.get())
        selected_spacing = self.spacing.get()
        selected_scaling = self.scaling.get()
        selected_input_dir = self.input.get()
        selected_model_path = self.model.get()
        selected_flag_path = self.flags.get()

        if selected_scaling == "EFOV":
            calculate_batch_efov(
                selected_input_dir,
                selected_model_path,
                selected_depth,
                selected_muscle
                )

        else:
            calculate_batch(
                selected_input_dir,
                selected_flag_path,
                selected_model_path,
                selected_depth,
                selected_spacing,
                selected_muscle,
                selected_scaling
                )

    def do_break(self):
        raise NotImplementedError()


if __name__ == "__main__":
    root = Tk()
    DeepACSA(root)
    root.mainloop()
