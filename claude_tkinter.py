import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from typing import List, Optional


class GUIApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("データ処理アプリケーション")
        self.root.geometry("800x600")

        # 状態管理用の変数
        self.excel_path: Optional[str] = None
        self.data_files: List[str] = []
        self.is_processing = False

        self.create_widgets()

    def create_widgets(self):
        # メインフレームの作成
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(expand=True, fill="both")

        # ノートブック（タブコンテナ）の作成
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(expand=True, fill="both", pady=(0, 10))

        # タブ1の作成
        self.tab1 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab1, text="データ処理")

        # コメント欄
        comment_frame = ttk.LabelFrame(self.tab1, text="処理内容", padding="5")
        comment_frame.pack(fill="x", padx=5, pady=5)

        self.comment_text = tk.Text(comment_frame, height=3, wrap="word")
        self.comment_text.pack(fill="x", padx=5, pady=5)
        self.comment_text.insert(
            "1.0", "このタブではエクセルファイルとデータファイルを選択して処理を実行します。"
        )

        # エクセルファイル選択部分
        excel_frame = ttk.LabelFrame(self.tab1, text="エクセルファイル", padding="5")
        excel_frame.pack(fill="x", padx=5, pady=5)

        self.excel_path_var = tk.StringVar()
        excel_path_entry = ttk.Entry(
            excel_frame, textvariable=self.excel_path_var, state="readonly"
        )
        excel_path_entry.pack(side="left", fill="x", expand=True, padx=(5, 5))

        self.excel_button = ttk.Button(excel_frame, text="エクセル選択", command=self.select_excel)
        self.excel_button.pack(side="right", padx=5)

        # データファイル選択部分
        data_frame = ttk.LabelFrame(self.tab1, text="データファイル", padding="5")
        data_frame.pack(fill="x", padx=5, pady=5)

        self.data_files_text = tk.Text(data_frame, height=5, state="disabled")
        self.data_files_text.pack(fill="x", padx=5, pady=5)

        self.data_button = ttk.Button(
            data_frame, text="データファイル選択", command=self.select_data_files, state="disabled"
        )
        self.data_button.pack(side="right", padx=5)

        # 進捗表示部分
        self.progress_frame = ttk.LabelFrame(self.tab1, text="状態", padding="5")
        self.progress_frame.pack(fill="x", padx=5, pady=5)

        # 固定の高さを確保するためのフレーム
        content_frame = ttk.Frame(self.progress_frame, height=80)
        content_frame.pack(fill="x", padx=5, pady=5)
        content_frame.pack_propagate(False)  # フレームサイズを固定

        # ガイダンス表示用のフレーム
        self.guidance_frame = ttk.Frame(content_frame)
        self.guidance_frame.pack(fill="both", expand=True)

        self.guidance_label = ttk.Label(
            self.guidance_frame,
            text="1. エクセルファイルを選択してください\n"
            + "2. データファイルを選択してください\n"
            + "3. 実行ボタンを押して処理を開始してください",
        )
        self.guidance_label.pack(pady=10)

        # 進捗表示用のフレーム（初期状態では非表示）
        self.progress_display_frame = ttk.Frame(content_frame)

        self.progress_var = tk.StringVar(value="待機中")
        self.progress_label = ttk.Label(self.progress_display_frame, textvariable=self.progress_var)
        self.progress_label.pack(fill="x", padx=5, pady=(5, 10))

        self.progress_bar = ttk.Progressbar(self.progress_display_frame, mode="determinate")
        self.progress_bar.pack(fill="x", padx=5, pady=(0, 5))

        # ボタン配置フレーム
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x", pady=5)

        # 左側のボタン
        left_button_frame = ttk.Frame(button_frame)
        left_button_frame.pack(side="left")

        self.execute_button = ttk.Button(
            left_button_frame, text="実行", command=self.execute_process, state="disabled"
        )
        self.execute_button.pack(side="left", padx=5)

        self.clear_button = ttk.Button(
            left_button_frame, text="クリア", command=self.clear_selections
        )
        self.clear_button.pack(side="left", padx=5)

        # 右側のボタン
        self.close_button = ttk.Button(button_frame, text="閉じる", command=self.root.destroy)
        self.close_button.pack(side="right", padx=5)

    def select_excel(self):
        file_path = filedialog.askopenfilename(
            title="エクセルファイルを選択", filetypes=[("Excel files", "*.xlsx *.xls")]
        )
        if file_path:
            self.excel_path = file_path
            self.excel_path_var.set(file_path)
            self.data_button.config(state="normal")
            self.update_execute_button()
            self.update_guidance()

    def select_data_files(self):
        files = filedialog.askopenfilenames(
            title="データファイルを選択", filetypes=[("All files", "*.*")]
        )
        if files:
            self.data_files = list(files)
            self.data_files_text.config(state="normal")
            self.data_files_text.delete("1.0", tk.END)
            self.data_files_text.insert("1.0", "\n".join(self.data_files))
            self.data_files_text.config(state="disabled")
            self.update_execute_button()
            self.update_guidance()

    def update_execute_button(self):
        if self.excel_path and self.data_files:
            self.execute_button.config(state="normal")
        else:
            self.execute_button.config(state="disabled")

    def update_guidance(self):
        if not self.excel_path:
            guidance_text = "1. エクセルファイルを選択してください"
        elif not self.data_files:
            guidance_text = "2. データファイルを選択してください"
        else:
            guidance_text = "3. 実行ボタンを押して処理を開始してください"

        self.guidance_label.config(text=guidance_text)

    def clear_selections(self):
        self.excel_path = None
        self.data_files = []
        self.excel_path_var.set("")
        self.data_files_text.config(state="normal")
        self.data_files_text.delete("1.0", tk.END)
        self.data_files_text.config(state="disabled")
        self.data_button.config(state="disabled")
        self.execute_button.config(state="disabled")

        # 進捗表示をガイダンス表示に戻す
        self.progress_display_frame.pack_forget()
        self.guidance_frame.pack(fill="both", expand=True)
        self.guidance_label.config(
            text="1. エクセルファイルを選択してください\n"
            + "2. データファイルを選択してください\n"
            + "3. 実行ボタンを押して処理を開始してください"
        )
        self.progress_bar["value"] = 0

    def execute_process(self):
        # 処理開始時にボタンを非アクティブ化
        self.set_widgets_state("disabled")
        self.is_processing = True

        # ガイダンス表示を進捗表示に切り替え
        self.guidance_frame.pack_forget()
        self.progress_display_frame.pack(fill="both", expand=True)

        # ここに実際の処理を実装
        # 例としてプログレスバーを動かす処理
        self.process_data()

    def process_data(self):
        total_files = len(self.data_files)
        for i, file in enumerate(self.data_files, 1):
            # 実際の処理をここに実装
            self.progress_var.set(f"処理中... ({i}/{total_files})")
            self.progress_bar["value"] = (i / total_files) * 100
            self.root.update()

        self.progress_var.set("処理完了")
        self.is_processing = False
        # 処理完了時にボタンを再度アクティブ化（クリアボタンと実行ボタン）
        self.set_widgets_state("normal")

    def set_widgets_state(self, state: str):
        widgets = [
            self.excel_button,
            self.data_button,
            self.execute_button,
            self.clear_button,
            self.comment_text,
        ]
        for widget in widgets:
            if widget.winfo_exists():
                if isinstance(widget, tk.Text):
                    widget.config(state=state)
                else:
                    widget.config(state=state)


if __name__ == "__main__":
    root = tk.Tk()
    app = GUIApp(root)
    root.mainloop()
