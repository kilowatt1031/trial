"""tkinterによるGUIコードサンプル."""

import time
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

WINDOW_SIZE = "800x600"
DEFAULT_PADDING = 5


class GUIApp:
    """メインGUIアプリケーションクラス.

    タブベースのGUIアプリケーションを管理し、共通のウィジェットを提供します。

    Attributes:
        root (tk.Tk): メインウィンドウ
        notebook (ttk.Notebook): タブコンテナ

    """

    def __init__(self, root: tk.Tk) -> None:
        """初期化処理.

        Args:
            root (tk.Tk): _description_

        """
        self.root = root
        self.root.title("データ処理アプリケーション")
        self.root.geometry(WINDOW_SIZE)

        # タブの処理状態を管理する辞書を初期化
        self.processing_tabs = {}

        # 終了時の処理を設定
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.create_widgets()

    def create_widgets(self) -> None:
        """tabを作れる状態として、クローズボタンを設定."""
        # メインフレームの作成
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(expand=True, fill="both")

        # ノートブック タブコンテナの作成
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(expand=True, fill="both", pady=(0, 10))

        # タブの作成 個々への配置の順番でタブの順番が決定
        self.analysis_tab = Ananlysis(self)
        self.processing_tabs["データ処理"] = self.analysis_tab  # タブを処理管理に追加
        self.tab2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab2, text="データ2")

        # ボタン配置フレーム
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x", pady=DEFAULT_PADDING)
        self.close_button = ttk.Button(
            button_frame,
            text="閉じる",
            command=self.root.destroy,
        )
        self.close_button.pack(side="right", padx=DEFAULT_PADDING)

    def check_processing_status(self) -> bool:
        """全タブの処理状態をチェック.

        Returns:
            bool: いずれかのタブが処理中の場合はTrue

        """
        for tab in self.processing_tabs.values():
            if hasattr(tab, "is_processing") and tab.is_processing:
                return True
        return False

    def get_processing_tab_names(self) -> list:
        """処理中のタブ名のリストを取得.

        Returns:
            list: 処理中のタブ名のリスト

        """
        processing_tabs = []
        for name, tab in self.processing_tabs.items():
            if hasattr(tab, "is_processing") and tab.is_processing:
                processing_tabs.append(name)
        return processing_tabs

    def on_closing(self) -> None:
        """アプリケーション終了時の処理."""
        if self.check_processing_status():
            # 処理中のタブ名を取得してメッセージに含める
            processing_tab_names = self.get_processing_tab_names()
            message = (
                "以下のタブで処理が実行中です:\n"
                f"{', '.join(processing_tab_names)}\n\n"
                "終了してもよろしいですか?"
            )

            if messagebox.askokcancel("確認", message):
                self.root.destroy()
        else:
            self.root.destroy()


class Ananlysis:
    """解析用のGUI処理.

    Attributes:
        excel_path (pathtib_Path):

    """

    def __init__(self, guiapp: ttk) -> None:
        """イニシャル処理.

        notebookを受け取り、タブを作成。GUIを作成する
        Args:
            notebook (ttk.Notebook): _description_
        """
        self.guiapp = guiapp
        # 状態管理用の変数
        self.excel_path = None
        self.data_files = []
        self.is_processing = False
        self.guidance_texts = [
            "1. エクセルファイルを選択してください",
            "2. データファイルを選択してください",
            "3. 実行ボタンを押して処理を開始してください",
        ]

        # タブ作成
        # notebookにフレームを作成
        self.analysis_tab = ttk.Frame(self.guiapp.notebook)
        # 作成したフレームをタブとして追加
        self.guiapp.notebook.add(self.analysis_tab, text="データ処理")

        # analysis_tabの処理
        self.create_tab_widgets()

    def create_tab_widgets(self) -> None:
        """widgetsの作成."""
        # コメント欄を作成
        # フレーム作成
        # paddingで内側の全体の余白を5に設定
        # 上下、左右や、上下左右バラバラで設定することも可能
        comment_frame = ttk.Frame(
            self.analysis_tab,
            padding=DEFAULT_PADDING,
        )
        # fill引数でx方向に引き延ばす
        # padxとpadyでこのフレームの外側の余白を作る
        comment_frame.pack(fill="x", padx=DEFAULT_PADDING, pady=DEFAULT_PADDING)
        # テキストを入れる場所
        # heightで3行を設定
        # wrapで折り返しありを設定
        # 背景をrootの波形と同じにする 引数か何かで取得する必要がある
        # テキスト部の凹みをフラットにする
        self.comment_text = tk.Text(
            comment_frame,
            height=3,
            wrap="word",
            bg=self.guiapp.root.cget("bg"),
            relief="flat",
        )
        self.comment_text.pack(fill="x", padx=DEFAULT_PADDING, pady=DEFAULT_PADDING)
        self.comment_text.insert(
            "1.0",
            "このタブではエクセルファイルと\nデータファイルを選択して処理を実行します。",
        )

        # エクセルファイル選択部分
        excel_frame = ttk.LabelFrame(
            self.analysis_tab,
            text="エクセルファイル",
            padding=DEFAULT_PADDING,
        )
        excel_frame.pack(fill="x", padx=DEFAULT_PADDING, pady=DEFAULT_PADDING)
        # エクセルパス用の変数引き渡し文字列の作成 ここにダイアログで選択した文字列を入れ
        # パス名を表示欄となるEntryに渡し、パスを表示させる
        self.excel_path_var = tk.StringVar()
        excel_path_entry = ttk.Entry(
            excel_frame,
            textvariable=self.excel_path_var,
            state="readonly",
        )
        excel_path_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(DEFAULT_PADDING, DEFAULT_PADDING),
        )

        self.excel_button = ttk.Button(
            excel_frame,
            text="エクセル選択",
            command=self.select_excel,
        )
        self.excel_button.pack(side="right", padx=DEFAULT_PADDING)

        # データファイル選択部分
        data_frame = ttk.LabelFrame(
            self.analysis_tab,
            text="データファイル",
            padding=DEFAULT_PADDING,
        )
        data_frame.pack(fill="x", padx=DEFAULT_PADDING, pady=DEFAULT_PADDING)

        self.data_files_text = tk.Text(data_frame, height=10, state="disabled")
        self.data_files_text.pack(
            side="left",
            fill="x",
            expand=True,
            padx=DEFAULT_PADDING,
            pady=DEFAULT_PADDING,
        )

        self.data_button = ttk.Button(
            data_frame,
            text="データファイル選択",
            command=self.select_data_files,
            state="disabled",
        )
        self.data_button.pack(side="right", padx=DEFAULT_PADDING)

        # 進捗表示部分のフレーム
        self.progress_frame = ttk.LabelFrame(
            self.analysis_tab,
            text="STATUS",
            padding=DEFAULT_PADDING,
        )
        self.progress_frame.pack(fill="x", padx=DEFAULT_PADDING, pady=DEFAULT_PADDING)
        # 固定の高さを確保するためのフレーム
        content_frame = ttk.Frame(self.progress_frame, height=80)
        content_frame.pack(fill="x", padx=DEFAULT_PADDING, pady=DEFAULT_PADDING)
        content_frame.pack_propagate(flag=False)  # フレームサイズを固定

        # ガイダンス表示用のフレーム
        self.guidance_frame = ttk.Frame(content_frame)
        self.guidance_frame.pack(fill="both", expand=True)
        # ガイダンスのテキストウィジェット
        self.guidance_label = ttk.Label(
            self.guidance_frame,
            text=(
                "1. エクセルファイルを選択してください\n"
                "2. データファイルを選択してください\n"
                "3. 実行ボタンを押して処理を開始してください"
            ),
        )
        self.guidance_label.pack(pady=10)

        # 進捗表示用のフレーム 初期状態では非表示
        self.progress_display_frame = ttk.Frame(content_frame)
        # 進捗表示用のテキストウィジェット
        self.progress_var = tk.StringVar(value="待機中")
        self.progress_label = ttk.Label(
            self.progress_display_frame,
            textvariable=self.progress_var,
        )
        self.progress_label.pack(fill="x", padx=DEFAULT_PADDING, pady=(DEFAULT_PADDING, 10))
        # プログレスバーウィジェット
        self.progress_bar = ttk.Progressbar(self.progress_display_frame, mode="determinate")
        self.progress_bar.pack(fill="x", padx=DEFAULT_PADDING, pady=(0, DEFAULT_PADDING))

        # ボタン配置フレーム
        button_frame = ttk.Frame(self.analysis_tab)
        button_frame.pack(fill="x", pady=DEFAULT_PADDING)
        # 実行ボタン
        self.execute_button = ttk.Button(
            button_frame,
            text="実行",
            command=self.execute_process,
            state="disabled",
        )
        self.execute_button.pack(side="left", padx=DEFAULT_PADDING)
        # クリアボタン
        self.clear_button = ttk.Button(
            button_frame,
            text="クリア",
            command=self.clear_selections,
        )
        self.clear_button.pack(side="left", padx=DEFAULT_PADDING)

    def select_excel(self) -> None:
        """エクセルファイル選択ダイアログ."""
        try:
            file_path = filedialog.askopenfilename(
                title="エクセルファイルを選択",
                filetypes=[("Excel files", "*.xlsx *.xls")],
            )
            if file_path:
                self.excel_path = file_path
                self.excel_path_var.set(file_path)
                self.data_button.config(state="normal")
                self.update_execute_button()
                self.update_guidance()
        except Exception as e:  # noqa: BLE001
            messagebox.showerror("エラー", f"ファイル選択中にエラーが発生しました: {e}")

    def select_data_files(self) -> None:
        """データファイルを複数選択ダイアログ."""
        files = filedialog.askopenfilenames(
            title="データファイルを選択",
            filetypes=[("All files", "*.*")],
        )
        if files:
            self.data_files = list(files)
            # データファイルのテキストエリアをアクティブ
            self.data_files_text.config(state="normal")
            # データファイルのテキストエリアクリア
            self.data_files_text.delete("1.0", tk.END)
            # データファイルのテキストエリアにファイルパスを表示
            self.data_files_text.insert("1.0", "\n".join(self.data_files))
            # データファイルのテキストエリアをディアクティブ
            self.data_files_text.config(state="disabled")
            self.update_execute_button()
            self.update_guidance()

    def update_execute_button(self) -> None:
        """実行ボタンのstate設定."""
        if self.excel_path and self.data_files:
            self.execute_button.config(state="normal")
        else:
            self.execute_button.config(state="disabled")

    def update_guidance(self) -> None:
        """ガイダンスをアップデータさせる."""
        if not self.excel_path:
            guidance_text = "1. エクセルファイルを選択してください"
        elif not self.data_files:
            guidance_text = "2. データファイルを選択してください"
        else:
            guidance_text = "3. 実行ボタンを押して処理を開始してください"

        self.guidance_label.config(text=guidance_text)

    def clear_selections(self) -> None:
        """クリアボタンを押したときの処理."""
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
            text=(
                "1. エクセルファイルを選択してください\n"
                "2. データファイルを選択してください\n"
                "3. 実行ボタンを押して処理を開始してください"
            ),
        )
        self.progress_bar["value"] = 0

    def execute_process(self) -> None:
        """ボタンが押されたときの処理."""
        # 処理開始時にボタンを非アクティブ化
        self.set_widgets_state("disabled")
        self.is_processing = True

        # ガイダンス表示を進捗表示に切り替え
        self.guidance_frame.pack_forget()
        self.progress_display_frame.pack(fill="both", expand=True)

        # ここに実際の処理を実装
        try:
            # 例としてプログレスバーを動かす処理
            self.process_data()
            self.progress_var.set("処理完了")
        except Exception as e:  # noqa: BLE001
            self.progress_var.set("エラーが発生しました")
            messagebox.showerror("エラー", f"処理中にエラーが発生しました: {e}")
        finally:
            self.is_processing = False
            # 処理完了時にボタンを再度アクティブ化 クリアボタンと実行ボタン
            self.set_widgets_state("normal")

    def process_data(self) -> None:
        """ここ進捗バーのレートを算出.

        ここに実行したプロセスを当てはめる。
        引数はselfを渡し、インスタンスとして受け取る
        """
        total_files = len(self.data_files)
        for i, file in enumerate(self.data_files, 1):
            # 実際の処理をここに実装
            self.progress_var.set(f"処理中... ({i}/{total_files})")
            self.progress_bar["value"] = (i / total_files) * 100
            self.analysis_tab.update()
            time.sleep(1)

    def set_widgets_state(self, state: str) -> None:
        """widegetsのstateを一括で変換.

        Args:
            state (str): 変換したい状態("normal" or "disabled")

        """
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
    app.root.mainloop()
