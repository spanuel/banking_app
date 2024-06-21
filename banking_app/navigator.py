def navigate_to(screen_function, root, *args, **kwargs):
    for widget in root.winfo_children():
        widget.destroy()
    screen_function(root, *args, **kwargs)