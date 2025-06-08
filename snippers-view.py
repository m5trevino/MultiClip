import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Any, Callable, Optional, List, Tuple
import pyperclip
from shared.snippets_manager import SnippetsManager, SnippetCommand, SnippetCategory

class VariableSubstitutionDialog:
    def __init__(self, parent, command: SnippetCommand):
        self.parent = parent
        self.command = command
        self.result = None
        self.variables = {}
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Variable Substitution")
        self.dialog.geometry("500x400")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self._create_ui()
        self.dialog.protocol("WM_DELETE_WINDOW", self._on_cancel)
        
        # Center on parent
        self.dialog.geometry("+%d+%d" % (
            parent.winfo_rootx() + 50,
            parent.winfo_rooty() + 50
        ))
    
    def _create_ui(self):
        main_frame = ttk.Frame(self.dialog, padding=10)
        main_frame.pack(fill='both', expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Enter Variable Values", 
                               font=('Arial', 12, 'bold'))
        title_label.pack(pady=(0, 10))
        
        # Command preview
        cmd_frame = ttk.LabelFrame(main_frame, text="Command Template", padding=5)
        cmd_frame.pack(fill='x', pady=(0, 10))
        
        cmd_text = tk.Text(cmd_frame, height=3, wrap='word', font=('Consolas', 10))
        cmd_text.pack(fill='x')
        cmd_text.insert('1.0', self.command.content)
        cmd_text.config(state='disabled')
        
        # Description if available
        if self.command.description:
            desc_label = ttk.Label(cmd_frame, text=f"Description: {self.command.description}",
                                  font=('Arial', 9), foreground='gray')
            desc_label.pack(anchor='w', pady=(5, 0))
        
        # Variables input
        vars_frame = ttk.LabelFrame(main_frame, text="Variables", padding=5)
        vars_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        # Scrollable frame for variables
        canvas = tk.Canvas(vars_frame)
        scrollbar = ttk.Scrollbar(vars_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Create variable inputs
        self.var_entries = {}
        for i, var_name in enumerate(self.command.variables):
            var_frame = ttk.Frame(scrollable_frame)
            var_frame.pack(fill='x', pady=2)
            
            label = ttk.Label(var_frame, text=f"{var_name}:", width=15)
            label.pack(side='left')
            
            entry = ttk.Entry(var_frame, width=40)
            entry.pack(side='left', padx=(5, 0), fill='x', expand=True)
            
            self.var_entries[var_name] = entry
            
            # Focus first entry
            if i == 0:
                entry.focus_set()
        
        # Preview frame
        preview_frame = ttk.LabelFrame(main_frame, text="Command Preview", padding=5)
        preview_frame.pack(fill='x', pady=(0, 10))
        
        self.preview_text = tk.Text(preview_frame, height=3, wrap='word', 
                                   font=('Consolas', 10), state='disabled')
        self.preview_text.pack(fill='x')
        
        # Bind entries to update preview
        for entry in self.var_entries.values():
            entry.bind('<KeyRelease>', self._update_preview)
        
        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill='x')
        
        ttk.Button(btn_frame, text="Cancel", command=self._on_cancel).pack(side='right')
        ttk.Button(btn_frame, text="Copy to Clipboard", 
                  command=self._on_copy_clipboard).pack(side='right', padx=(0, 5))
        ttk.Button(btn_frame, text="Send to Slot", 
                  command=self._on_send_slot).pack(side='right', padx=(0, 5))
        
        self._update_preview()
    
    def _update_preview(self, event=None):
        # Get current variable values
        current_vars = {}
        for var_name, entry in self.var_entries.items():
            current_vars[var_name] = entry.get()
        
        # Generate preview
        preview = self.command.substitute_variables(current_vars)
        
        self.preview_text.config(state='normal')
        self.preview_text.delete('1.0', 'end')
        self.preview_text.insert('1.0', preview)
        self.preview_text.config(state='disabled')
        
        self.current_command = preview
    
    def _on_copy_clipboard(self):
        if hasattr(self, 'current_command'):
            pyperclip.copy(self.current_command)
            self.command.use()  # Increment usage count
            self.result = ("clipboard", self.current_command)
            self.dialog.destroy()
    
    def _on_send_slot(self):
        if hasattr(self, 'current_command'):
            # This would need a callback to the main system
            self.command.use()
            self.result = ("slot", self.current_command)
            self.dialog.destroy()
    
    def _on_cancel(self):
        self.dialog.destroy()
    
    def show(self):
        self.dialog.wait_window()
        return self.result

class SnippersViewWindow:
    def __init__(self, snippets_manager: SnippetsManager):
        self.snippets_manager = snippets_manager
        self.root = tk.Tk()
        self.root.title("Snippers - Command Library")
        self.root.geometry("800x600")
        
        # Callbacks
        self.command_select_callback: Optional[Callable] = None
        
        self._create_ui()
    
    def _create_ui(self):
        # Main paned window
        paned = ttk.PanedWindow(self.root, orient='horizontal')
        paned.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Left panel - category tree
        left_frame = ttk.Frame(paned)
        paned.add(left_frame, weight=1)
        
        # Search frame
        search_frame = ttk.Frame(left_frame)
        search_frame.pack(fill='x', pady=(0, 5))
        
        ttk.Label(search_frame, text="Search:").pack(side='left')
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side='left', fill='x', expand=True, padx=(5, 0))
        search_entry.bind('<KeyRelease>', self._on_search)
        
        # Category tree
        tree_frame = ttk.LabelFrame(left_frame, text="Categories", padding=5)
        tree_frame.pack(fill='both', expand=True)
        
        self.category_tree = ttk.Treeview(tree_frame, selectmode='single')
        self.category_tree.pack(fill='both', expand=True)
        
        # Tree scrollbar
        tree_scroll = ttk.Scrollbar(tree_frame, orient='vertical', 
                                   command=self.category_tree.yview)
        tree_scroll.pack(side='right', fill='y')
        self.category_tree.configure(yscrollcommand=tree_scroll.set)
        
        self.category_tree.bind('<<TreeviewSelect>>', self._on_category_select)
        
        # Right panel - commands list and details
        right_frame = ttk.Frame(paned)
        paned.add(right_frame, weight=2)
        
        # Commands list
        cmd_frame = ttk.LabelFrame(right_frame, text="Commands", padding=5)
        cmd_frame.pack(fill='both', expand=True)
        
        # Commands listbox with scrollbar
        cmd_list_frame = ttk.Frame(cmd_frame)
        cmd_list_frame.pack(fill='both', expand=True)
        
        self.commands_listbox = tk.Listbox(cmd_list_frame, font=('Consolas', 10))
        cmd_scroll = ttk.Scrollbar(cmd_list_frame, orient='vertical',
                                  command=self.commands_listbox.yview)
        
        self.commands_listbox.pack(side='left', fill='both', expand=True)
        cmd_scroll.pack(side='right', fill='y')
        self.commands_listbox.configure(yscrollcommand=cmd_scroll.set)
        
        self.commands_listbox.bind('<<ListboxSelect>>', self._on_command_select)
        self.commands_listbox.bind('<Double-Button-1>', self._on_command_double_click)
        
        # Command details
        details_frame = ttk.LabelFrame(right_frame, text="Command Details", padding=5)
        details_frame.pack(fill='x', pady=(5, 0))
        
        self.details_text = tk.Text(details_frame, height=8, wrap='word',
                                   font=('Consolas', 10), state='disabled')
        self.details_text.pack(fill='x')
        
        # Action buttons
        btn_frame = ttk.Frame(details_frame)
        btn_frame.pack(fill='x', pady=(5, 0))
        
        ttk.Button(btn_frame, text="Use Command", 
                  command=self._use_selected_command).pack(side='left')
        ttk.Button(btn_frame, text="Copy Raw", 
                  command=self._copy_raw_command).pack(side='left', padx=(5, 0))
        ttk.Button(btn_frame, text="Edit", 
                  command=self._edit_command).pack(side='right')
        ttk.Button(btn_frame, text="Delete", 
                  command=self._delete_command).pack(side='right', padx=(0, 5))
        
        self._populate_tree()
    
    def _populate_tree(self):
        # Clear existing items
        for item in self.category_tree.get_children():
            self.category_tree.delete(item)
        
        # Add categories
        for category in self.snippets_manager.root_categories:
            self._add_category_to_tree(category, "")
    
    def _add_category_to_tree(self, category: SnippetCategory, parent: str):
        item_id = self.category_tree.insert(parent, 'end', text=category.name,
                                           values=(category.id,))
        
        # Add subcategories
        for subcat in category.subcategories:
            self._add_category_to_tree(subcat, item_id)
        
        # If category has commands, show count
        if category.commands:
            self.category_tree.set(item_id, 'text', f"{category.name} ({len(category.commands)})")
    
    def _on_category_select(self, event):
        selection = self.category_tree.selection()
        if selection:
            item_id = selection[0]
            category_id = self.category_tree.item(item_id, 'values')[0]
            
            # Find the category and show its commands
            category = self._find_category_by_id(category_id)
            if category:
                self._show_category_commands(category)
    
    def _find_category_by_id(self, category_id: str) -> Optional[SnippetCategory]:
        def search_category(cat: SnippetCategory) -> Optional[SnippetCategory]:
            if cat.id == category_id:
                return cat
            for subcat in cat.subcategories:
                result = search_category(subcat)
                if result:
                    return result
            return None
        
        for root_cat in self.snippets_manager.root_categories:
            result = search_category(root_cat)
            if result:
                return result
        return None
    
    def _show_category_commands(self, category: SnippetCategory):
        self.commands_listbox.delete(0, 'end')
        self.current_category = category
        
        for cmd in category.commands:
            display_text = cmd.content
            if len(display_text) > 80:
                display_text = display_text[:77] + "..."
            
            if cmd.description:
                display_text += f" // {cmd.description}"
            
            self.commands_listbox.insert('end', display_text)
    
    def _on_command_select(self, event):
        selection = self.commands_listbox.curselection()
        if selection and hasattr(self, 'current_category'):
            cmd_index = selection[0]
            if cmd_index < len(self.current_category.commands):
                cmd = self.current_category.commands[cmd_index]
                self._show_command_details(cmd)
    
    def _show_command_details(self, command: SnippetCommand):
        self.current_command = command
        
        details = f"Command: {command.content}\n\n"
        
        if command.description:
            details += f"Description: {command.description}\n\n"
        
        if command.variables:
            details += f"Variables: {', '.join(command.variables)}\n\n"
        
        details += f"Usage Count: {command.usage_count}\n"
        details += f"Created: {command.created_at.strftime('%Y-%m-%d %H:%M') if command.created_at else 'Unknown'}\n"
        
        if command.last_used:
            details += f"Last Used: {command.last_used.strftime('%Y-%m-%d %H:%M')}\n"
        
        self.details_text.config(state='normal')
        self.details_text.delete('1.0', 'end')
        self.details_text.insert('1.0', details)
        self.details_text.config(state='disabled')
    
    def _on_command_double_click(self, event):
        self._use_selected_command()
    
    def _use_selected_command(self):
        if hasattr(self, 'current_command'):
            if self.current_command.variables:
                # Show variable substitution dialog
                dialog = VariableSubstitutionDialog(self.root, self.current_command)
                result = dialog.show()
                
                if result and self.command_select_callback:
                    action, command = result
                    self.command_select_callback(action, command)
            else:
                # No variables, copy directly
                pyperclip.copy(self.current_command.content)
                self.current_command.use()
                
                if self.command_select_callback:
                    self.command_select_callback("clipboard", self.current_command.content)
    
    def _copy_raw_command(self):
        if hasattr(self, 'current_command'):
            pyperclip.copy(self.current_command.content)
            messagebox.showinfo("Copied", "Raw command copied to clipboard")
    
    def _edit_command(self):
        if hasattr(self, 'current_command'):
            # This would launch the snippers-save dialog in edit mode
            messagebox.showinfo("Edit", "Edit functionality would open snippers-save")
    
    def _delete_command(self):
        if hasattr(self, 'current_command') and hasattr(self, 'current_category'):
            if messagebox.askyesno("Confirm Delete", 
                                 f"Delete command: {self.current_command.content[:50]}...?"):
                self.current_category.remove_command(self.current_command.id)
                self._show_category_commands(self.current_category)
                self.details_text.config(state='normal')
                self.details_text.delete('1.0', 'end')
                self.details_text.config(state='disabled')
    
    def _on_search(self, event):
        query = self.search_var.get().strip()
        if query:
            self._show_search_results(query)
        else:
            self._populate_tree()
    
    def _show_search_results(self, query: str):
        results = self.snippets_manager.search_all_commands(query)
        
        self.commands_listbox.delete(0, 'end')
        self.search_results = results
        
        for cmd, path in results:
            display_text = f"[{path}] {cmd.content}"
            if len(display_text) > 80:
                display_text = display_text[:77] + "..."
            
            if cmd.description:
                display_text += f" // {cmd.description}"
            
            self.commands_listbox.insert('end', display_text)
        
        # Update tree selection label
        if hasattr(self, 'category_tree'):
            # Could highlight search results in tree
            pass
    
    def set_command_select_callback(self, callback: Callable):
        self.command_select_callback = callback
    
    def run(self):
        self.root.mainloop()
    
    def destroy(self):
        self.root.destroy()

# Standalone launcher
if __name__ == "__main__":
    from shared.snippets_manager import SnippetsManager
    
    manager = SnippetsManager()
    window = SnippersViewWindow(manager)
    window.run()
