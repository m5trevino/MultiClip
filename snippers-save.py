import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Any, Callable, Optional, List
import re
from shared.snippets_manager import SnippetsManager, SnippetCommand, SnippetCategory

class SnippersSaveWindow:
    def __init__(self, snippets_manager: SnippetsManager, command_to_edit: Optional[SnippetCommand] = None):
        self.snippets_manager = snippets_manager
        self.command_to_edit = command_to_edit
        self.is_editing = command_to_edit is not None
        
        self.root = tk.Tk()
        self.root.title("Save Snippet" if not self.is_editing else "Edit Snippet")
        self.root.geometry("600x500")
        
        # Callbacks
        self.save_callback: Optional[Callable] = None
        
        self._create_ui()
        
        if self.is_editing:
            self._populate_edit_data()
    
    def _create_ui(self):
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill='both', expand=True)
        
        # Title
        title_text = "Edit Snippet" if self.is_editing else "Save New Snippet"
        title_label = ttk.Label(main_frame, text=title_text, 
                               font=('Arial', 14, 'bold'))
        title_label.pack(pady=(0, 15))
        
        # Command input
        cmd_frame = ttk.LabelFrame(main_frame, text="Command", padding=5)
        cmd_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Label(cmd_frame, text="Enter your command (use 'var' for variables):").pack(anchor='w')
        
        self.command_text = tk.Text(cmd_frame, height=4, wrap='word', 
                                   font=('Consolas', 11))
        self.command_text.pack(fill='x', pady=(5, 0))
cmd_scroll = ttk.Scrollbar(cmd_frame, orient='vertical', 
                                 command=self.command_text.yview)
       cmd_scroll.pack(side='right', fill='y')
       self.command_text.configure(yscrollcommand=cmd_scroll.set)
       
       self.command_text.bind('<KeyRelease>', self._on_command_change)
       
       # Description input
       desc_frame = ttk.LabelFrame(main_frame, text="Description (Optional)", padding=5)
       desc_frame.pack(fill='x', pady=(0, 10))
       
       self.description_var = tk.StringVar()
       desc_entry = ttk.Entry(desc_frame, textvariable=self.description_var, 
                             font=('Arial', 10))
       desc_entry.pack(fill='x')
       
       # Variables detection
       vars_frame = ttk.LabelFrame(main_frame, text="Detected Variables", padding=5)
       vars_frame.pack(fill='x', pady=(0, 10))
       
       self.variables_label = ttk.Label(vars_frame, text="No variables detected", 
                                       font=('Arial', 10), foreground='gray')
       self.variables_label.pack(anchor='w')
       
       # Category selection
       cat_frame = ttk.LabelFrame(main_frame, text="Category", padding=5)
       cat_frame.pack(fill='x', pady=(0, 10))
       
       # Category dropdown
       cat_select_frame = ttk.Frame(cat_frame)
       cat_select_frame.pack(fill='x')
       
       ttk.Label(cat_select_frame, text="Select category:").pack(side='left')
       
       self.category_var = tk.StringVar()
       self.category_combo = ttk.Combobox(cat_select_frame, textvariable=self.category_var,
                                         state='readonly', width=30)
       self.category_combo.pack(side='left', padx=(10, 0), fill='x', expand=True)
       
       # New category frame
       new_cat_frame = ttk.Frame(cat_frame)
       new_cat_frame.pack(fill='x', pady=(5, 0))
       
       self.new_category_var = tk.StringVar()
       self.new_cat_check = ttk.Checkbutton(new_cat_frame, text="Create new category:", 
                                           command=self._toggle_new_category)
       self.new_cat_check.pack(side='left')
       
       self.new_cat_entry = ttk.Entry(new_cat_frame, textvariable=self.new_category_var,
                                     state='disabled', width=30)
       self.new_cat_entry.pack(side='left', padx=(10, 0), fill='x', expand=True)
       
       # Subcategory input
       subcat_frame = ttk.Frame(cat_frame)
       subcat_frame.pack(fill='x', pady=(5, 0))
       
       ttk.Label(subcat_frame, text="Subcategory (optional):").pack(side='left')
       self.subcategory_var = tk.StringVar()
       subcat_entry = ttk.Entry(subcat_frame, textvariable=self.subcategory_var, width=30)
       subcat_entry.pack(side='left', padx=(10, 0), fill='x', expand=True)
       
       # Preview frame
       preview_frame = ttk.LabelFrame(main_frame, text="Preview", padding=5)
       preview_frame.pack(fill='both', expand=True, pady=(0, 10))
       
       self.preview_text = tk.Text(preview_frame, height=4, wrap='word',
                                  font=('Consolas', 10), state='disabled',
                                  bg='#f8f8f8')
       self.preview_text.pack(fill='both', expand=True)
       
       # Buttons
       btn_frame = ttk.Frame(main_frame)
       btn_frame.pack(fill='x')
       
       ttk.Button(btn_frame, text="Cancel", command=self._on_cancel).pack(side='right')
       
       save_text = "Update" if self.is_editing else "Save"
       ttk.Button(btn_frame, text=save_text, 
                 command=self._on_save).pack(side='right', padx=(0, 10))
       
       ttk.Button(btn_frame, text="Test Variables", 
                 command=self._test_variables).pack(side='left')
       
       self._populate_categories()
       self._update_preview()
   
   def _populate_categories(self):
       categories = []
       for root_cat in self.snippets_manager.root_categories:
           categories.append(root_cat.name)
           for subcat in root_cat.subcategories:
               categories.append(f"{root_cat.name}/{subcat.name}")
       
       self.category_combo['values'] = categories
       if categories:
           self.category_combo.set(categories[0])
   
   def _populate_edit_data(self):
       if self.command_to_edit:
           # Fill in the command content
           self.command_text.insert('1.0', self.command_to_edit.content)
           
           # Fill in description
           if self.command_to_edit.description:
               self.description_var.set(self.command_to_edit.description)
           
           self._on_command_change()
   
   def _toggle_new_category(self):
       if self.new_cat_check.instate(['selected']):
           self.new_cat_entry.config(state='normal')
           self.category_combo.config(state='disabled')
       else:
           self.new_cat_entry.config(state='disabled')
           self.category_combo.config(state='readonly')
   
   def _on_command_change(self, event=None):
       command_content = self.command_text.get('1.0', 'end-1c')
       
       # Detect variables
       var_count = command_content.count('var')
       if var_count > 0:
           vars_text = f"Detected {var_count} variable(s): "
           vars_text += ", ".join([f"var{i+1}" for i in range(var_count)])
           self.variables_label.config(text=vars_text, foreground='blue')
       else:
           self.variables_label.config(text="No variables detected", foreground='gray')
       
       self._update_preview()
   
   def _update_preview(self):
       command_content = self.command_text.get('1.0', 'end-1c')
       description = self.description_var.get()
       
       # Create temporary command for preview
       temp_cmd = SnippetCommand(command_content, description)
       
       preview_text = f"Command: {temp_cmd.content}\n"
       
       if description:
           preview_text += f"Description: {description}\n"
       
       if temp_cmd.variables:
           preview_text += f"Variables: {', '.join(temp_cmd.variables)}\n"
       
       # Show category path
       category_path = self._get_target_category_path()
       if category_path:
           preview_text += f"Category: {category_path}\n"
       
       # Show example with variables filled
       if temp_cmd.variables:
           example_vars = {var: f"<{var}>" for var in temp_cmd.variables}
           example_command = temp_cmd.substitute_variables(example_vars)
           preview_text += f"\nExample: {example_command}"
       
       self.preview_text.config(state='normal')
       self.preview_text.delete('1.0', 'end')
       self.preview_text.insert('1.0', preview_text)
       self.preview_text.config(state='disabled')
   
   def _get_target_category_path(self) -> str:
       if self.new_cat_check.instate(['selected']):
           new_cat = self.new_category_var.get().strip()
           if new_cat:
               subcat = self.subcategory_var.get().strip()
               return f"{new_cat}/{subcat}" if subcat else new_cat
       else:
           selected_cat = self.category_var.get()
           if selected_cat:
               subcat = self.subcategory_var.get().strip()
               return f"{selected_cat}/{subcat}" if subcat else selected_cat
       return ""
   
   def _test_variables(self):
       command_content = self.command_text.get('1.0', 'end-1c')
       if not command_content.strip():
           messagebox.showwarning("Warning", "Please enter a command first")
           return
       
       temp_cmd = SnippetCommand(command_content)
       
       if not temp_cmd.variables:
           messagebox.showinfo("Info", "No variables detected in this command")
           return
       
       # Create a simple test dialog
       test_dialog = tk.Toplevel(self.root)
       test_dialog.title("Test Variables")
       test_dialog.geometry("400x300")
       test_dialog.transient(self.root)
       test_dialog.grab_set()
       
       frame = ttk.Frame(test_dialog, padding=10)
       frame.pack(fill='both', expand=True)
       
       ttk.Label(frame, text="Enter test values:", font=('Arial', 11, 'bold')).pack(pady=(0, 10))
       
       test_entries = {}
       for var in temp_cmd.variables:
           var_frame = ttk.Frame(frame)
           var_frame.pack(fill='x', pady=2)
           
           ttk.Label(var_frame, text=f"{var}:", width=10).pack(side='left')
           entry = ttk.Entry(var_frame, width=30)
           entry.pack(side='left', padx=(5, 0))
           test_entries[var] = entry
       
       result_frame = ttk.LabelFrame(frame, text="Result", padding=5)
       result_frame.pack(fill='both', expand=True, pady=(10, 0))
       
       result_text = tk.Text(result_frame, height=4, wrap='word', 
                            font=('Consolas', 10), state='disabled')
       result_text.pack(fill='both', expand=True)
       
       def update_test():
           test_vars = {var: entry.get() for var, entry in test_entries.items()}
           result = temp_cmd.substitute_variables(test_vars)
           
           result_text.config(state='normal')
           result_text.delete('1.0', 'end')
           result_text.insert('1.0', result)
           result_text.config(state='disabled')
       
       for entry in test_entries.values():
           entry.bind('<KeyRelease>', lambda e: update_test())
       
       ttk.Button(frame, text="Close", command=test_dialog.destroy).pack(pady=(10, 0))
   
   def _on_save(self):
       command_content = self.command_text.get('1.0', 'end-1c').strip()
       if not command_content:
           messagebox.showerror("Error", "Command cannot be empty")
           return
       
       description = self.description_var.get().strip()
       category_path = self._get_target_category_path()
       
       if not category_path:
           messagebox.showerror("Error", "Please select or create a category")
           return
       
       try:
           # Create the command
           if self.is_editing:
               # Update existing command
               self.command_to_edit.content = command_content
               self.command_to_edit.description = description
               self.command_to_edit.variables = self.command_to_edit._extract_variables(command_content)
               success = True
           else:
               # Create new command
               new_command = SnippetCommand(command_content, description)
               
               # Handle category creation/selection
               if self.new_cat_check.instate(['selected']):
                   # Create new category
                   new_cat_name = self.new_category_var.get().strip()
                   target_category = self.snippets_manager.add_root_category(new_cat_name)
               else:
                   # Find existing category
                   selected_path = self.category_var.get()
                   target_category = self.snippets_manager.find_category(selected_path)
               
               if target_category:
                   # Handle subcategory
                   subcat_name = self.subcategory_var.get().strip()
                   if subcat_name:
                       # Check if subcategory exists
                       subcat = None
                       for existing_subcat in target_category.subcategories:
                           if existing_subcat.name == subcat_name:
                               subcat = existing_subcat
                               break
                       
                       if not subcat:
                           # Create new subcategory
                           subcat = SnippetCategory(subcat_name)
                           target_category.add_subcategory(subcat)
                       
                       target_category = subcat
                   
                   target_category.add_command(new_command)
                   success = True
               else:
                   success = False
           
           if success:
               if self.save_callback:
                   self.save_callback(True)
               
               action = "updated" if self.is_editing else "saved"
               messagebox.showinfo("Success", f"Snippet {action} successfully!")
               self.root.destroy()
           else:
               messagebox.showerror("Error", "Failed to save snippet")
               
       except Exception as e:
           messagebox.showerror("Error", f"Error saving snippet: {str(e)}")
   
   def _on_cancel(self):
       if self._has_unsaved_changes():
           if messagebox.askyesno("Confirm", "Discard unsaved changes?"):
               self.root.destroy()
       else:
           self.root.destroy()
   
   def _has_unsaved_changes(self) -> bool:
       command_content = self.command_text.get('1.0', 'end-1c').strip()
       description = self.description_var.get().strip()
       
       if self.is_editing:
           return (command_content != self.command_to_edit.content or
                  description != (self.command_to_edit.description or ""))
       else:
           return bool(command_content or description)
   
   def set_save_callback(self, callback: Callable):
       self.save_callback = callback
   
   def run(self):
       self.root.mainloop()
   
   def destroy(self):
       self.root.destroy()

# Standalone launcher
if __name__ == "__main__":
   from shared.snippets_manager import SnippetsManager
   
   manager = SnippetsManager()
   window = SnippersSaveWindow(manager)
   window.run()
