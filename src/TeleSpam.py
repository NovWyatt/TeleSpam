import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, simpledialog, filedialog
from telethon import TelegramClient, functions, types
from telethon.errors import *
from telethon.tl.functions.channels import GetParticipantsRequest, GetParticipantRequest
from telethon.tl.types import ChannelParticipantsSearch
import asyncio
import os
import json
from datetime import datetime
import threading


class TelegramGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Telegram Sender")
        self.window.geometry("800x600")

        self.api_id = "25488940"
        self.api_hash = "a8a598f95be27d691aee44b3c16d8dfb"

        # Khởi tạo event loop và client
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.client = None
        self.logged_in = False
        self.target_groups = []

        # Start thread cho event loop
        self.loop_thread = threading.Thread(target=self._run_loop, daemon=True)
        self.loop_thread.start()

        self.load_groups()
        self.setup_gui()

    def _run_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    def load_groups(self):
        if os.path.exists("groups.json"):
            with open("groups.json", "r") as f:
                self.target_groups = json.load(f)

    def save_groups(self):
        with open("groups.json", "w") as f:
            json.dump(self.target_groups, f)

    def setup_gui(self):
        # Thiết lập tabs
        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=5)

        self.login_frame = ttk.Frame(self.notebook)
        self.sender_frame = ttk.Frame(self.notebook)
        self.group_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.login_frame, text="Đăng nhập")
        self.notebook.add(self.sender_frame, text="Gửi tin nhắn", state="disabled")
        self.notebook.add(self.group_frame, text="Quản lý nhóm", state="disabled")

        self.setup_login_tab()
        self.setup_sender_tab()
        self.setup_group_tab()

        # Khu vực log
        self.log_area = scrolledtext.ScrolledText(self.window, height=10)
        self.log_area.pack(fill="both", expand=True, padx=10, pady=5)

    def setup_login_tab(self):
        frame = ttk.LabelFrame(self.login_frame, text="Đăng nhập", padding=10)
        frame.pack(fill="both", expand=True, padx=10, pady=5)

        ttk.Label(frame, text="Số điện thoại:").grid(
            row=0, column=0, sticky="w", pady=5
        )
        self.phone_entry = ttk.Entry(frame)
        self.phone_entry.grid(row=0, column=1, sticky="ew", pady=5)

        self.login_button = ttk.Button(
            frame, text="Đăng nhập", command=self.start_login
        )
        self.login_button.grid(row=1, column=0, columnspan=2, pady=10)

        self.logout_button = ttk.Button(
            frame, text="Đăng xuất", command=self.logout, state="disabled"
        )
        self.logout_button.grid(row=2, column=0, columnspan=2, pady=5)

    def setup_sender_tab(self):
        frame = ttk.LabelFrame(self.sender_frame, text="Gửi tin nhắn", padding=10)
        frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.target_var = tk.StringVar(value="1")
        ttk.Radiobutton(
            frame,
            text="Dùng danh sách nhóm đã cấu hình",
            variable=self.target_var,
            value="1",
        ).pack()
        ttk.Radiobutton(
            frame, text="Chọn từ danh sách chat", variable=self.target_var, value="2"
        ).pack()

        ttk.Label(frame, text="Nội dung tin nhắn:").pack(anchor="w", pady=5)
        self.message_entry = scrolledtext.ScrolledText(frame, height=5)
        self.message_entry.pack(fill="both", expand=True)

        controls_frame = ttk.Frame(frame)
        controls_frame.pack(fill="x", pady=10)

        ttk.Label(controls_frame, text="Số lượng:").pack(side="left")
        self.count_entry = ttk.Entry(controls_frame, width=10)
        self.count_entry.pack(side="left", padx=5)

        ttk.Label(controls_frame, text="Độ trễ (giây):").pack(side="left")
        self.delay_entry = ttk.Entry(controls_frame, width=10)
        self.delay_entry.pack(side="left", padx=5)

        self.spam_type = tk.StringVar(value="1")
        ttk.Radiobutton(
            frame, text="Spam nhóm", variable=self.spam_type, value="1"
        ).pack()
        ttk.Radiobutton(
            frame, text="Spam thành viên", variable=self.spam_type, value="2"
        ).pack()

        self.send_button = ttk.Button(
            frame, text="Gửi tin nhắn", command=self.start_sending
        )
        self.send_button.pack(pady=10)
        image_frame = ttk.Frame(frame)
        image_frame.pack(fill="x", pady=5)

        self.image_path = tk.StringVar()
        ttk.Label(image_frame, text="Hình ảnh:").pack(side="left")
        self.image_entry = ttk.Entry(
            image_frame, textvariable=self.image_path, state="readonly"
        )
        self.image_entry.pack(side="left", fill="x", expand=True, padx=5)

        def choose_image():
            file_path = filedialog.askopenfilename(
                filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")]
            )
            if file_path:
                self.image_path.set(file_path)

        ttk.Button(image_frame, text="Chọn ảnh", command=choose_image).pack(
            side="right"
        )

    def setup_group_tab(self):
        frame = ttk.LabelFrame(self.group_frame, text="Quản lý nhóm", padding=10)
        frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.groups_listbox = tk.Listbox(frame, height=10)
        self.groups_listbox.pack(fill="both", expand=True)

        controls_frame = ttk.Frame(frame)
        controls_frame.pack(fill="x", pady=10)

        self.group_entry = ttk.Entry(frame)
        self.group_entry.pack(fill="x", pady=5)

        ttk.Button(controls_frame, text="Thêm nhóm", command=self.add_group).pack(
            side="left", padx=5
        )
        ttk.Button(controls_frame, text="Xóa nhóm", command=self.remove_group).pack(
            side="left"
        )

        self.update_groups_list()

    def log(self, message):
        self.log_area.insert(tk.END, f"{message}\n")
        self.log_area.see(tk.END)

    def update_groups_list(self):
        self.groups_listbox.delete(0, tk.END)
        for group in self.target_groups:
            self.groups_listbox.insert(tk.END, group)

    def add_group(self):
        group = self.group_entry.get().strip()
        if group and group not in self.target_groups:
            self.target_groups.append(group)
            self.save_groups()
            self.update_groups_list()
            self.group_entry.delete(0, tk.END)
            self.log(f"Đã thêm nhóm: {group}")
        else:
            messagebox.showwarning("Cảnh báo", "Nhóm không hợp lệ hoặc đã tồn tại!")

    def remove_group(self):
        selection = self.groups_listbox.curselection()
        if selection:
            group = self.target_groups.pop(selection[0])
            self.save_groups()
            self.update_groups_list()
            self.log(f"Đã xóa nhóm: {group}")
        else:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một nhóm để xóa!")

    def start_login(self):
        phone = self.phone_entry.get().strip()
        if phone:
            self.login_button.config(state="disabled")
            self.log("Đang xử lý đăng nhập...")
            future = asyncio.run_coroutine_threadsafe(self.login(phone), self.loop)
            self.window.after(100, self.check_login, future)
        else:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập số điện thoại!")

    def check_login(self, future):
        if not future.done():
            self.window.after(100, self.check_login, future)
            return
        try:
            result = future.result()
            if result:
                self.login_button.config(state="disabled")
                self.logout_button.config(state="normal")
                self.notebook.tab(1, state="normal")
                self.notebook.tab(2, state="normal")
            else:
                self.login_button.config(state="normal")
        except Exception as e:
            self.login_button.config(state="normal")
            messagebox.showerror("Lỗi", f"Lỗi đăng nhập: {str(e)}")

    async def login(self, phone):
        try:
            self.client = TelegramClient(phone, self.api_id, self.api_hash)
            await self.client.connect()

            if not await self.client.is_user_authorized():
                await self.client.send_code_request(phone)
                self.window.after(100, self.request_code, phone)
                return False

            self.logged_in = True
            self.log("Đăng nhập thành công!")
            return True

        except Exception as e:
            self.log(f"Lỗi đăng nhập: {str(e)}")
            return False

        except Exception as e:
            messagebox.showerror("Lỗi", f"Đăng nhập thất bại: {str(e)}")
            self.log(f"Lỗi đăng nhập: {str(e)}")

    def request_code(self, phone):
        code = simpledialog.askstring("Xác thực", "Nhập mã xác thực bạn nhận được:")
        if code:
            future = asyncio.run_coroutine_threadsafe(
                self.verify_code(phone, code), self.loop
            )
            self.window.after(100, self.check_login, future)

    async def verify_code(self, phone, code):
        try:
            await self.client.sign_in(phone, code)
            self.logged_in = True
            self.log("Đăng nhập thành công!")
            return True
        except Exception as e:
            self.log(f"Lỗi xác thực: {str(e)}")
        return False

    def logout(self):
        if self.client:
            self.client.disconnect()
        self.client = None
        self.logged_in = False
        self.login_button.config(state="normal")
        self.logout_button.config(state="disabled")
        self.notebook.tab(1, state="disabled")
        self.notebook.tab(2, state="disabled")
        self.log("Đã đăng xuất!")

    def start_sending(self):
        if not self.logged_in:
            messagebox.showwarning("Cảnh báo", "Vui lòng đăng nhập trước!")
            return

        try:
            count = int(self.count_entry.get())
            delay = float(self.delay_entry.get())
            message = self.message_entry.get("1.0", tk.END).strip()

            if not message:
                messagebox.showwarning("Cảnh báo", "Vui lòng nhập nội dung tin nhắn!")
                return

            future = asyncio.run_coroutine_threadsafe(
                self.send_messages(message, count, delay), self.loop
            )
            self.window.after(100, self.check_send, future)

        except ValueError:
            messagebox.showerror("Lỗi", "Số lượng hoặc độ trễ không hợp lệ!")

    def check_send(self, future):
        if not future.done():
            self.window.after(100, self.check_send, future)
            return
        try:
            future.result()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi gửi tin nhắn: {str(e)}")

    async def send_messages(self, message, count, delay):
        try:
            if self.target_var.get() == "1":
                targets = await self.get_target_groups()
            else:
                targets = await self.select_from_dialogs()

            if not targets:
                self.log("Không tìm thấy mục tiêu nào!")
                return

            if self.spam_type.get() == "2":
                all_users = []
                for target in targets:
                    users = await self.get_all_users(target)
                    all_users.extend(users)
                targets = all_users

            total_success = 0
            total_failed = 0

            self.log(f"Bắt đầu gửi tin nhắn đến {len(targets)} mục tiêu...")

            for target in targets:
                success = 0
                failed = 0

                for i in range(count):
                    try:
                        if self.image_path.get():
                            await self.client.send_file(
                                target,
                                self.image_path.get(),
                                caption=message if message else None,
                            )
                        else:
                            await self.client.send_message(target, message)

                        success += 1
                        total_success += 1
                        self.log(f"Gửi tin nhắn thành công ({success}/{count})")
                        await asyncio.sleep(delay)

                    except Exception as e:
                        failed += 1
                        total_failed += 1
                        self.log(f"Gửi tin nhắn thất bại: {str(e)}")

                self.log(
                    f"Kết quả cho mục tiêu: Thành công={success}, Thất bại={failed}"
                )

            self.log(
                f"Kết quả cuối cùng: Tổng thành công={total_success}, Tổng thất bại={total_failed}"
            )

        except Exception as e:
            self.log(f"Lỗi trong quá trình gửi: {str(e)}")

    async def get_all_users(self, entity):
        all_users = []
        try:
            offset = 0
            limit = 100

            while True:
                participants = await self.client(
                    GetParticipantsRequest(
                        entity, ChannelParticipantsSearch(""), offset, limit, hash=0
                    )
                )
                if not participants.users:
                    break
                all_users.extend(participants.users)
                offset += len(participants.users)
                self.log(f"Đã tìm thấy {len(all_users)} thành viên...")
                await asyncio.sleep(0.5)

        except Exception as e:
            self.log(f"Lỗi khi lấy danh sách thành viên: {str(e)}")
        return all_users

    async def get_target_groups(self):
        if not self.target_groups:
            self.log("Không tìm thấy nhóm nào đã cấu hình!")
            return []

        entities = []
        for target in self.target_groups:
            try:
                entity = await self.client.get_entity(target)
                entities.append(entity)
                self.log(f"Đã tìm thấy nhóm: {getattr(entity, 'title', target)}")
            except Exception as e:
                self.log(f"Lỗi khi xử lý {target}: {str(e)}")
        return entities

    async def select_from_dialogs(self):
        try:
            dialogs = await self.client.get_dialogs()
            # Tạo cửa sổ mới
            dialog_window = tk.Toplevel(self.window)
            dialog_window.title("Danh sách chat")
            dialog_window.geometry("400x600")
            # Tạo listbox
            listbox = tk.Listbox(dialog_window, selectmode="multiple")
            listbox.pack(fill="both", expand=True)
            dialog_list = []
            for i, dialog in enumerate(dialogs):
                name = getattr(dialog.entity, "title", dialog.name)
                listbox.insert(tk.END, f"{i}: {name}")
                dialog_list.append(dialog.entity)

            # Nút xác nhận
            def confirm():
                selections = listbox.curselection()
                dialog_window.selected_entities = [dialog_list[i] for i in selections]
                dialog_window.destroy()

            ttk.Button(dialog_window, text="Xác nhận", command=confirm).pack(pady=10)
            # Chờ cửa sổ đóng
            self.window.wait_window(dialog_window)
            return getattr(dialog_window, "selected_entities", [])
        except Exception as e:
            self.log(f"Lỗi khi lấy danh sách chat: {str(e)}")
            messagebox.showerror("Lỗi", "Không thể lấy danh sách chat!")
            return []


def main():
    app = TelegramGUI()
    app.window.mainloop()


if __name__ == "__main__":
    main()
