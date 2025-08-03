import tkinter as tk
from tkinter import PhotoImage
import csv
import webbrowser
import random
import os
import re

# --- رنگ‌های اصلی رابط کاربری ---
THEME_COLOR = "#000080"           # رنگ آبی تیره برای نوار بالا و دکمه‌ها
BG_COLOR = "#FAFDFF"              # رنگ پس‌زمینه اصلی صفحه
DISCOUNT_BAR_COLOR = "#16aefc"    # رنگ نوار تخفیف

# --- لیست کالاهای تخفیفی و قیمت‌های ویژه ---
DISCOUNTED_PRODUCTS = {
    "موبایل سامسونگ گلکسی": {
        "original": "30,000,000",     # قیمت اصلی بدون تخفیف
        "discounted": "27,000,000"    # قیمت پس از 10٪ تخفیف
    },
    "لپ‌تاپ اپل مک‌بوک": {
        "original": "70,000,000",
        "discounted": "66,500,000"    # 5٪ تخفیف
    },
    "تبلت سامسونگ تب ": {
        "original": "25,000,000",
        "discounted": "21,250,000"    # 15٪ تخفیف (نام با فاصله اضافه)
    },
    "هدفون بلوتوثی سونی": {
        "original": "12,000,000",
        "discounted": "9,600,000"     # 20٪ تخفیف
    },
    "  ساعت اپل واچ   ": {
        "original": "15,000,000",
        "discounted": "13,800,000"    # 8٪ تخفیف (نام با فاصله قبل و بعد)
    }
}

# --- تابع اصلی: نمایش پروفایل کاربر ---
def show_profile_window():
    """
    پنجره پروفایل کاربر را باز می‌کند.
    اگر کاربر وارد نشده باشد، پیام خطا نمایش داده می‌شود.
    اگر کاربر مدیر باشد، به جای پروفایل، صفحه مدیریت باز می‌شود.
    """
    # بررسی وضعیت ورود کاربر
    if not current_user:
        messagebox.showerror("خطا", "لطفاً ابتدا وارد حساب کاربری خود شوید.")
        return

    # اگر کاربر نقش مدیر داشته باشد، به صفحه مدیریت هدایت شود
    if current_user["role"] == "admin":
        show_admin_panel()
        return

    # ایجاد پنجره پروفایل کاربر
    profile_win = tk.Toplevel()
    profile_win.title("پروفایل کاربری")
    center_window(profile_win, 1000, 600)
    profile_win.configure(bg="#eeeeee")
    profile_win.resizable(False, False)

    # --- نوار بالایی ---
    nav_bar = tk.Frame(profile_win, bg=THEME_COLOR, height=80)
    nav_bar.pack(fill="x", side="top")

    # لوگوی در سمت راست
    try:
        nav_logo = PhotoImage(file="shopera_nav_logo.png")
        logo_label = tk.Label(nav_bar, image=nav_logo, bg=THEME_COLOR)
        logo_label.image = nav_logo
    except:
        logo_label = tk.Label(nav_bar, text="Shopera", font=("Arial", 16, "bold"), fg="white", bg=THEME_COLOR)
    logo_label.pack(side="right", padx=10)

    # دکمه بازگشت در سمت چپ
    back_frame = tk.Frame(nav_bar, bg=THEME_COLOR)
    back_frame.pack(side="left", padx=10)
    try:
        back_img = PhotoImage(file="backright.png").subsample(2, 2)
        back_btn = tk.Button(back_frame, image=back_img, bg=THEME_COLOR, bd=0, command=profile_win.destroy)
        back_btn.image = back_img
    except:
        back_btn = tk.Button(back_frame, text="بازگشت", font=("Arial", 11), bg=THEME_COLOR, fg="white", bd=0, command=profile_win.destroy)
    back_btn.pack(side="left", padx=5)

    # --- عنوان صفحه ---
    tk.Label(profile_win, text=" پروفایل کاربری", font=("Arial", 18, "bold"), fg=THEME_COLOR, bg="#eeeeee").pack(pady=15)

    # --- فریم اصلی محتوا ---
    main_frame = tk.Frame(profile_win, bg="#eeeeee")
    main_frame.pack(fill="both", expand=True, padx=30, pady=(10, 80))

    # --- سمت راست: اطلاعات کاربر ---
    info_frame = tk.Frame(main_frame, bg="white", bd=0, relief="solid", width=300)
    info_frame.pack(side="right", fill="y", padx=(0, 20))
    info_frame.pack_propagate(False)

    # --- نمایش عکس کاربر بر اساس جنسیت ---
    gender = current_user.get("gender", "ناشناس")
    gender_icon_file = "woman.png" if gender == "زن" else "man.png" if gender == "مرد" else "person.png"

    try:
        profile_photo = PhotoImage(file=gender_icon_file)
        photo_label = tk.Label(info_frame, image=profile_photo, bg="white")
        photo_label.image = profile_photo
        photo_label.pack(pady=(20, 10))
    except Exception as e:
        default_text = "👩" if gender == "زن" else "👨" if gender == "مرد" else "👤"
        photo_label = tk.Label(info_frame, text=default_text, font=("Arial", 40), bg="white")
        photo_label.pack(pady=(20, 10))

    # --- نمایش اطلاعات شخصی کاربر ---
    tk.Label(info_frame, text="اطلاعات شما", font=("Arial", 14, "bold"), bg="white").pack(pady=10)
    tk.Label(info_frame, text=f"نام: {current_user['firstname']}", font=("Arial", 12), bg="white").pack(anchor="e", padx=20, pady=5)
    tk.Label(info_frame, text=f"نام خانوادگی: {current_user['lastname']}", font=("Arial", 12), bg="white").pack(anchor="e", padx=20, pady=5)
    tk.Label(info_frame, text=f"نام کاربری: {current_user['username']}", font=("Arial", 12), bg="white").pack(anchor="e", padx=20, pady=5)
    tk.Label(info_frame, text=f"موجودی: {current_user['balance']:,} تومان", font=("Arial", 12), bg="white").pack(anchor="e", padx=20, pady=5)
    tk.Label(info_frame, text=f"جنسیت: {gender}", font=("Arial", 12), bg="white").pack(anchor="e", padx=20, pady=5)

    # --- سمت چپ: نمایش سفارشات قبلی ---
    orders_frame = tk.Frame(main_frame, bg="#eeeeee")
    orders_frame.pack(side="left", fill="both", expand=True)

    tk.Label(orders_frame, text="سفارشات قبلی شما", font=("Arial", 14, "bold"), bg="#eeeeee").pack(anchor="e", pady=(10, 10), padx=28)

    # --- تابع بارگذاری و نمایش سفارشات ---
    def load_and_display_orders():
        """
        سفارشات کاربر را از فایل orders.csv می‌خواند و نمایش می‌دهد.
        اگر سفارشی نداشته باشد، پیام مناسب نمایش داده می‌شود.
        """
        # پاک کردن سفارشات قبلی از صفحه
        for widget in orders_frame.winfo_children():
            if isinstance(widget, tk.Frame) and widget != orders_frame.pack_slaves()[0]:  # غیر از عنوان
                widget.destroy()

        try:
            with open('orders.csv', 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                user_orders = []
                for row in reader:
                    cleaned_row = {k.strip(): v for k, v in row.items()}
                    if '\ufeffusername' in cleaned_row:
                        cleaned_row['username'] = cleaned_row.pop('\ufeffusername')
                    if cleaned_row['username'] == current_user['username']:
                        user_orders.append({
                            "product": cleaned_row['product_id'].split('_')[0],
                            "quantity": cleaned_row['quantity'],
                            "total_price": cleaned_row['total_price'],
                            "date": cleaned_row['date'],
                            "full_row": cleaned_row  # برای حذف از فایل
                        })
        except Exception as e:
            messagebox.showerror("خطا", f"خطا در خواندن سفارشات: {e}")
            return

        if not user_orders:
            tk.Label(orders_frame, text="هنوز سفارشی ثبت نکرده‌اید.", font=("Arial", 11), bg="white", fg="gray").pack(anchor="e", padx=10, pady=5)
            return

        # نمایش هر سفارش در یک فریم جداگانه
        for order in user_orders:
            order_frame = tk.Frame(orders_frame, bg="white", bd=0, relief="solid")
            order_frame.pack(fill="x", pady=8, padx=20)

            info_frame_inner = tk.Frame(order_frame, bg="white")
            info_frame_inner.pack(side="right", padx=15, pady=10)

            tk.Label(info_frame_inner, text=f"نام کالا: {order['product']}", font=("Arial", 11), bg="white").pack(anchor="e", pady=2)
            tk.Label(info_frame_inner, text=f"تعداد: {order['quantity']}", font=("Arial", 11), bg="white").pack(anchor="e", pady=2)
            tk.Label(info_frame_inner, text=f"قیمت کل: {int(order['total_price']):,} تومان", font=("Arial", 11), bg="white").pack(anchor="e", pady=2)
            tk.Label(info_frame_inner, text=f"تاریخ: {order['date']}", font=("Arial", 11), bg="white").pack(anchor="e", pady=2)

            # دکمه حذف سفارش
            def make_delete(order_row, frame):
                return lambda: delete_order(order_row, frame)

            delete_btn = tk.Button(
                order_frame,
                text="حذف سفارش",
                font=("Arial", 12, "bold"),
                bg=THEME_COLOR,
                fg="white",
                bd=0,
                highlightthickness=0,
                relief="flat",
                command=make_delete(order["full_row"], order_frame)
            )
            delete_btn.pack(side="left", padx=15, pady=10)

    # --- تابع حذف یک سفارش ---
    def delete_order(order_row, frame):
        """
        یک سفارش را از فایل orders.csv و رابط کاربری حذف می‌کند.
        ابتدا تأیید کاربر گرفته می‌شود.
        """
        if not messagebox.askyesno("تأیید حذف", "آیا از حذف این سفارش مطمئن هستید؟"):
            return

        try:
            # خواندن همه سفارشات
            with open('orders.csv', 'r', encoding='utf-8-sig') as f:
                rows = list(csv.DictReader(f))

            # فیلتر کردن سفارش مورد نظر
            filtered_rows = []
            removed = False
            for row in rows:
                if not (
                    row['username'] == order_row['username'] and
                    row['product_id'] == order_row['product_id'] and
                    row['quantity'] == order_row['quantity'] and
                    row['date'] == order_row['date'] and
                    row['total_price'] == order_row['total_price']
                ):
                    filtered_rows.append(row)
                else:
                    removed = True

            if not removed:
                messagebox.showwarning("هشدار", "سفارش یافت نشد.")
                return

            # نوشتن دوباره فایل بدون سفارش حذف شده
            with open('orders.csv', 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=['username', 'product_id', 'quantity', 'total_price', 'date'])
                writer.writeheader()
                writer.writerows(filtered_rows)

            # حذف ویجت از صفحه
            frame.destroy()
            messagebox.showinfo("موفقیت", "سفارش با موفقیت حذف شد.")

        except Exception as e:
            messagebox.showerror("خطا", f"حذف سفارش با خطا مواجه شد: {e}")

    # --- اولین بارگذاری سفارشات ---
    load_and_display_orders()

def get_user_full_name(username):
    """
    با استفاده از نام کاربری، نام و نام خانوادگی کاربر را از فایل users.csv برمی‌گرداند.
    اگر کاربر پیدا نشد، نام کاربری را برمی‌گرداند.
    """
    try:
        with open('users.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['username'] == username:
                    return f"{row['firstname']} {row['lastname']}".strip()
        return username  # اگر کاربر پیدا نشد، نام کاربری نمایش داده می‌شود
    except:
        return username  # در صورت خطا، نام کاربری نمایش داده می‌شود

def load_comments():
    """
    کامنت‌های کاربران را از فایل comments.csv می‌خواند.
    اگر فایل وجود نداشت، لیستی از کامنت‌های پیش‌فرض برمی‌گرداند.
    """
    comments = []
    try:
        with open('comments.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if 'comment' in row and row['comment'].strip():
                    comments.append(row['comment'])
    except FileNotFoundError:
        # اگر فایل وجود نداشت، کامنت‌های پیش‌فرض نمایش داده می‌شوند
        comments = [
            "عالی بود، ممنون از اطلاعات خوبتون!",
            "محصول کیفیت خوبی داشت و به موقع ارسال شد.",
            "امیدوارم در آینده امکانات بیشتری اضافه بشه.",
            "کاش تخفیف بیشتری داشت.",
            "بسته‌بندی خیلی خوبی داشت، راضی بودم.",
            "پشتیبانی خیلی سریع پاسخ داد.",
            "کاملاً با عکس مطابقت داشت.",
            "ارسال با کمی تأخیر انجام شد ولی ارزشش رو داشت.",
            "کیفیت ساخت واقعا بالاست.",
            "برای بار دوم هم از این فروشگاه خرید کردم و راضی‌ام."
        ]
    except Exception as e:
        print(f"خطای خواندن کامنت‌ها: {e}")
        comments = []  # در صورت خطا، لیست خالی برمی‌گردد
    return comments

def save_comment(comment):
    """
    یک کامنت جدید را به فایل comments.csv اضافه می‌کند.
    """
    try:
        with open('comments.csv', 'a', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([comment])
    except Exception as e:
        print(f"خطای ذخیره کامنت: {e}")

def save_order_to_csv(username, product_id, quantity, total_price, date):
    """
    یک سفارش جدید را به فایل orders.csv اضافه می‌کند.
    اگر فایل وجود نداشته باشد، ابتدا هدر می‌نویسد.
    """
    file_exists = os.path.isfile('orders.csv')
    with open('orders.csv', 'a', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["username", "product_id", "quantity", "total_price", "date"])
        if not file_exists:
            writer.writeheader()  # نوشتن هدر در صورت اولین بار بودن فایل
        writer.writerow({
            "username": username,
            "product_id": product_id,
            "quantity": quantity,
            "total_price": total_price,
            "date": date
        })

def get_product_name_by_id(product_id):
    """
    با استفاده از شناسه محصول (product_id)، نام محصول را از فایل products.csv برمی‌گرداند.
    اگر پیدا نشد، خود شناسه را برمی‌گرداند.
    """
    try:
        with open('products.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['product_id'] == product_id:
                    return row['name']
        return product_id  # اگر محصول پیدا نشد، شناسه نمایش داده می‌شود
    except:
        return product_id  # در صورت خطا، شناسه نمایش داده می‌شود

def save_users(users):
    """
    اطلاعات تمام کاربران را در فایل users.csv ذخیره می‌کند.
    شامل نام کاربری، رمز، موجودی، نقش، نام، نام خانوادگی و جنسیت.
    """
    with open('users.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['username', 'password', 'balance', 'role', 'firstname', 'lastname', 'gender'])
        writer.writeheader()
        for username, data in users.items():
            writer.writerow({
                'username': username,
                'password': data['password'],
                'balance': data['balance'],
                'role': data['role'],
                'firstname': data['firstname'],
                'lastname': data['lastname'],
                'gender': data.get('gender', 'ناشناس')  # اگر جنسیت نداشت، "ناشناس" ذخیره می‌شود
            })

def load_users():
    """
    اطلاعات کاربران را از فایل users.csv می‌خواند و در یک دیکشنری ذخیره می‌کند.
    """
    users = {}
    try:
        with open('users.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                users[row['username']] = {
                    'password': row['password'],
                    'balance': int(row['balance']),
                    'role': row['role'],
                    'firstname': row['firstname'],
                    'lastname': row['lastname'],
                    'gender': row['gender']  # جنسیت کاربر
                }
    except Exception as e:
        print(f"خطای خواندن users.csv: {e}")
    return users

# --- دیتابیس کاربران و متغیرهای سراسری ---
users_db = load_users()
default_mode = True
cart_items = []
current_user = None

# --- تابع مرکز کردن صفحه ها ---
def center_window(window, width, height):
    """
    یک پنجره را در مرکز صفحه نمایش قرار می‌دهد.
    """
    window.update_idletasks()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

# --------------------------- ساخت ورودی با Placeholder --------------------------- #
def create_entry_with_placeholder(parent, placeholder, show_char=None):
    """
    یک ویجت ورودی (Entry) با متن پیش‌فرض (placeholder) ایجاد می‌کند.
    هنگام کلیک، متن پیش‌فرض پاک شده و هنگام خروج بدون ورود متن، دوباره نمایش داده می‌شود.

    پارامترها:
    parent: ویجت والد (معمولاً یک Frame)
    placeholder: متنی که به عنوان راهنما نمایش داده می‌شود
    show_char: اگر مشخص شود، ورودی به صورت مخفی (مثل رمز عبور) نمایش داده می‌شود
    """
    entry = tk.Entry(
        parent,
        font=("Arial", 12),
        fg="gray",  # رنگ متن برای نمایش placeholder
        bg="white",
        relief="solid",
        bd=1,
        justify="right"
    )

    def on_focus_in(event):
        """هنگام فوکوس روی فیلد ورودی"""
        if entry.get() == placeholder:
            entry.delete(0, tk.END)  # پاک کردن متن پیش‌فرض
            if show_char:
                entry.config(show=show_char)  # نمایش کاراکترهای مخفی (مثل *)
            entry.config(fg=THEME_COLOR)  # تغییر رنگ متن به رنگ اصلی تم

    def on_focus_out(event):
        """هنگام خروج از فیلد ورودی"""
        if entry.get() == "":
            entry.insert(0, placeholder)  # بازگرداندن متن پیش‌فرض
            entry.config(show="")  # غیرفعال کردن نمایش کاراکتر ویژه
            entry.config(fg="gray")  # تغییر رنگ متن به خاکستری

    # تنظیم اولیه: قرار دادن متن پیش‌فرض
    entry.insert(0, placeholder)
    # اتصال رویدادها
    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)

    return entry

def show_product_details(product):
    """
    صفحه جزئیات یک محصول را باز می‌کند.
    شامل تصویر، قیمت، توضیحات و دکمه افزودن به سبد خرید می‌شود.
    """
    # ایجاد پنجره جدید برای نمایش جزئیات محصول
    detail_win = tk.Toplevel()
    center_window(detail_win, 1000, 600)
    detail_win.title(product.get('name', 'محصول بدون عنوان'))
    center_window(detail_win, 1000, 600)
    detail_win.configure(bg="white")
    detail_win.resizable(False, False)

    # --- نوار بالایی ---
    nav_bar = tk.Frame(detail_win, bg=THEME_COLOR, height=80)
    nav_bar.pack(fill="x", side="top")

    # لوگوی شرکت در سمت راست
    try:
        nav_logo = PhotoImage(file="shopera_nav_logo.png")
        logo_label = tk.Label(nav_bar, image=nav_logo, bg=THEME_COLOR)
        logo_label.image = nav_logo
    except:
        logo_label = tk.Label(nav_bar, text="Shopera", font=("Arial", 18, "bold"), fg="white", bg=THEME_COLOR)
    logo_label.pack(side="right", padx=10)

    # --- کادر جستجو ---
    search_frame = tk.Frame(nav_bar, bg="white", height=35)
    search_frame.pack(side="right", padx=10, pady=20)

    # ایجاد ورودی جستجو با قابلیت placeholder
    search_entry = tk.Entry(
        search_frame,
        font=("Arial", 12),
        fg="gray",
        bg="white",
        relief="flat",           # حذف حاشیه مستطیل
        bd=0,                    # حذف کامل حاشیه
        highlightthickness=0,    # غیرفعال کردن خط دور
        justify="right"
    )

    # اضافه کردن متن پیش‌فرض
    search_entry.insert(0, "جستجو...")

    # --- مدیریت متن پیش‌فرض (placeholder) ---
    def on_focus_in(event):
        """هنگام کلیک روی فیلد جستجو"""
        if search_entry.get() == "جستجو...":
            search_entry.delete(0, tk.END)
            search_entry.config(fg="black")

    def on_focus_out(event):
        """هنگام خروج از فیلد جستجو"""
        if search_entry.get() == "":
            search_entry.insert(0, "جستجو...")
            search_entry.config(fg="gray")

    # اتصال رویدادها به ورودی جستجو
    search_entry.bind("<FocusIn>", on_focus_in)
    search_entry.bind("<FocusOut>", on_focus_out)
    search_entry.pack(side="left", padx=(5, 0))

    # --- تابع انجام جستجو ---
    def perform_search():
        """جستجو بر اساس عبارت وارد شده و هدایت به دسته‌بندی مربوطه"""
        query = search_entry.get().strip()
        if query == "جستجو..." or not query:
            return

        # نقشه‌برداری از عبارات جستجو به دسته‌بندی‌ها
        category_mapping = {
            "موبایل": "موبایل",
            "موبايل": "موبایل",  # با ی عربی
            "گوشی": "موبایل",
            "گوشي": "موبایل",  # با ی عربی
            "mobile": "موبایل",
            "لپ تاپ": "لپ‌تاپ",
            "لپتاپ": "لپ‌تاپ",
            "لپ": "لپ‌تاپ",
            "هدفون": "هدفون",
            "هدست": "هدفون",
            "ساعت": "ساعت",
            "دیجیتال": "دیجیتال"
        }

        # نرمال‌سازی عبارت جستجو
        normalized_query = query.lower() \
            .replace(" ", "") \
            .replace("‌", "") \
            .replace("ي", "ی")

        # جستجو در نقشه‌برداری دسته‌بندی‌ها
        matched_category = None
        for key, value in category_mapping.items():
            normalized_key = key.lower() \
                .replace(" ", "") \
                .replace("‌", "") \
                .replace("ي", "ی")

            if normalized_query == normalized_key:
                matched_category = value
                break

        # نتیجه جستجو
        if matched_category:
            show_category_products(matched_category)
        else:
            messagebox.showinfo(
                "نتیجه جستجو",
                "عبارت مورد نظر یافت نشد."
            )

    # --- دکمه جستجو ---
    try:
        search_icon = PhotoImage(file="search_icon.png")
        search_btn = tk.Button(search_frame, image=search_icon, bg="white", bd=0, command=perform_search)
        search_btn.image = search_icon
    except:
        search_btn = tk.Button(search_frame, text="🔍", font=("Arial", 12), bg="white", bd=0, command=perform_search)
    search_btn.pack(side="right", padx=(0, 5))

    # --- فریم دکمه‌های سمت چپ ---
    buttons_frame = tk.Frame(nav_bar, bg=THEME_COLOR)
    buttons_frame.pack(side="left", padx=10)

    # --- دکمه بازگشت ---
    try:
        back_img = PhotoImage(file="backright.png").subsample(2, 2)
        back_btn = tk.Button(
            buttons_frame,
            image=back_img,
            bg=THEME_COLOR,  # رنگ پس‌زمینه دکمه
            activebackground=THEME_COLOR,  # رنگ هنگام کلیک
            bd=0,  # حذف حاشیه
            highlightthickness=0,  # حذف هایلایت
            relief="flat",  # حذف اثر سه بعدی
            command=detail_win.destroy  # بستن پنجره فعلی
        )
        back_btn.image = back_img
    except:
        # اگر تصویر بارگذاری نشد، دکمه متنی نمایش داده شود
        back_btn = tk.Button(
            buttons_frame,
            text="بازگشت",
            font=("Arial", 11),
            bg=THEME_COLOR,
            fg="white",
            activebackground=THEME_COLOR,
            activeforeground="white",
            bd=0,
            highlightthickness=0,
            relief="flat",
            command=detail_win.destroy
        )
    back_btn.pack(side="left", padx=5)

    # --- دکمه سبد خرید ---
    try:
        cart_img = PhotoImage(file="cart_icon.png")
        cart_btn = tk.Button(
            buttons_frame,
            image=cart_img,
            bg=THEME_COLOR,
            bd=0,
            command=show_cart_window  # باز کردن پنجره سبد خرید
        )
        cart_btn.image = cart_img
    except:
        # اگر تصویر بارگذاری نشد، آیکون یونیکد نمایش داده شود
        cart_btn = tk.Button(
            buttons_frame,
            text="🛒",
            font=("Arial", 14),
            bg=THEME_COLOR,
            fg="white",
            bd=0,
            command=show_cart_window
        )
    cart_btn.pack(side="left", padx=5)

    # --- فریم اصلی محتوای صفحه ---
    content_frame = tk.Frame(detail_win, bg="white")
    content_frame.pack(fill="both", expand=True)

    # --- نمایش تصویر محصول ---
    try:
        filename = os.path.basename(product.get("image", "default.png"))
        image_path = os.path.join("details", filename)
        img = tk.PhotoImage(file=image_path)
        img_label = tk.Label(content_frame, image=img, bg="white")
        img_label.image = img
    except:
        # اگر تصویر یافت نشد، پیام خطا نمایش داده شود
        img_label = tk.Label(content_frame, text="❌ تصویر یافت نشد", fg="red", bg="white", font=("arial", 14, "bold"))
    img_label.grid(row=0, column=2, padx=10, pady=9)

    # --- فریم مرکزی (نام، ویژگی‌ها، قیمت و دکمه خرید) ---
    center_frame = tk.Frame(content_frame, bg="white", width=300, height=490)
    center_frame.grid(row=0, column=1, padx=5, pady=10, sticky="n")
    center_frame.pack_propagate(False)

    # --- نام محصول ---
    tk.Label(center_frame, text=product.get("name", "بدون نام"),
             font=("arial", 17, "bold"), fg="#001F5B", bg="white").pack(pady=(30, 10))

    # --- کادر ویژگی‌های محصول ---
    features_box = tk.Frame(center_frame, bg="#f5f5f5")
    features_box.pack(pady=(20, 10), fill="x", padx=15)

    # لیست ویژگی‌ها از داده محصول
    features = product.get("features", [
        " صفحه نمایش: ۶.۵ اینچ •",
        " باتری: ۵۰۰۰ میلی‌آمپر •",
        " رم: ۸ گیگ •",
        " دوربین: ۶۴ مگاپیکسل •"
    ])

    # نمایش هر ویژگی
    for feat in features:
        lbl = tk.Label(features_box, text=feat, font=("arial", 14), bg="#f5f5f5",
                       anchor="e", justify="right")
        lbl.pack(anchor="e", padx=10, pady=2)

    # --- بخش انتخاب رنگ ---
    tk.Label(features_box, text=":رنگ‌ بندی", font=("arial", 14, "bold"),
             bg="#f5f5f5", fg=THEME_COLOR, anchor="e", justify="right").pack(anchor="e", pady=(10, 5), padx=10)

    color_frame = tk.Frame(features_box, bg="#f5f5f5")
    color_frame.pack(anchor="e", padx=10)

    # متغیر برای نگه‌داری رنگ انتخاب شده
    selected_color = tk.StringVar(value="")

    # تمام رنگ‌های ممکن
    all_colors = {
        "سفید": "#ffffff",
        "مشکی": "#000000",
        "طوسی": "#9e9e9e",
        "قرمز": "#e53935",
        "کرم": "#f5f5dc"
    }

    # رنگ‌های اجباری و اختیاری
    mandatory = ["سفید", "مشکی"]
    optional = ["طوسی", "قرمز", "کرم"]
    selected_names = mandatory + random.sample(optional, k=random.randint(0, len(optional)))
    selected_colors = [(name, all_colors[name]) for name in selected_names]

    # لیست دکمه‌های رنگ
    color_buttons = []

    def select_color(color, canvas, outline_id):
        """انتخاب یک رنگ و برجسته کردن آن"""
        selected_color.set(color)
        for c, cid in color_buttons:
            c.itemconfig(cid, width=1, outline="gray")
        canvas.itemconfig(outline_id, width=3, outline="#2196f3")

    # ایجاد دکمه برای هر رنگ
    for name, clr in selected_colors:
        canvas = tk.Canvas(color_frame, width=32, height=32, bg="#f5f5f5", highlightthickness=0)
        circle_id = canvas.create_oval(5, 5, 27, 27, fill=clr, outline="gray", width=1)
        canvas.bind("<Button-1>", lambda e, c=clr, cnv=canvas, cid=circle_id: select_color(c, cnv, cid))
        canvas.pack(side="right", padx=6, pady=5)
        color_buttons.append((canvas, circle_id))

    # --- بخش قیمت و دکمه افزودن به سبد خرید ---
    bottom_box = tk.Frame(center_frame, bg="#f5f5f5")
    bottom_box.pack(pady=(30, 10), fill="x", padx=10)

    # نمایش قیمت محصول
    price_text = product.get("price", "0")
    tk.Label(bottom_box, text=f"{price_text} تومان", font=("arial", 14, "bold"),
             bg="#f5f5f5", fg="black").pack(pady=(10, 5))

    # --- تابع افزودن به سبد خرید ---
    def handle_add_to_cart():
        """افزودن محصول به سبد خرید فقط در صورت انتخاب رنگ"""
        if selected_color.get():
            add_to_cart(product, selected_color.get())
            added_label.config(text=" به سبد خرید افزوده شد", fg="green")
        else:
            added_label.config(text=" لطفاً رنگ را انتخاب کنید", fg="red")

    # --- دکمه افزودن به سبد خرید ---
    tk.Button(bottom_box, text="افزودن به سبد خرید", font=("arial", 12, "bold"),
              bg="#2196f3", fg="white", height=2, width=25, cursor="hand2",
              command=handle_add_to_cart).pack(pady=(0, 10))

    # --- پیام تأیید یا خطا ---
    added_label = tk.Label(bottom_box, text="", font=("arial", 10), fg="green", bg="#f5f5f5")
    added_label.pack()
    # --- فریم سمت چپ (امتیاز و نظرات) ---
    left_frame = tk.Frame(content_frame, bg="#f9f9f9", width=270, height=400)
    left_frame.grid(row=0, column=0, padx=5, pady=(48, 25), sticky="n")
    left_frame.pack_propagate(False)

    # --- بسته‌بندی امتیاز و نظرات ---
    bottom_wrapper = tk.Frame(left_frame, bg="#f9f9f9")
    bottom_wrapper.pack(side="bottom", fill="x", pady=10)

    # --- بارگذاری تصاویر ستاره ---
    star_filled_img = PhotoImage(file="stars/star_filled.png")
    star_empty_img = PhotoImage(file="stars/star_empty.png")

    # --- امتیاز اولیه تصادفی و متغیر کنترلی ---
    initial_rating = random.randint(1, 5)
    user_rating = tk.IntVar(value=initial_rating)

    # --- فریم نمایش ستاره‌ها ---
    rating_frame = tk.Frame(bottom_wrapper, bg="#f9f9f9")
    rating_frame.pack(pady=(10, 5))

    # لیست برای نگه‌داری برچسب‌های ستاره
    star_labels = []

    def convert_to_persian(num):
        """
        یک عدد را به اعداد فارسی تبدیل می‌کند.
        """
        digits = "۰۱۲۳۴۵۶۷۸۹"
        return "".join(digits[int(d)] if d.isdigit() else d for d in str(num))

    def update_stars(rating):
        """
        وضعیت ستاره‌ها را بر اساس امتیاز کاربر به‌روز می‌کند.
        """
        user_rating.set(rating)
        for i, lbl in enumerate(star_labels):
            img = star_filled_img if i < rating else star_empty_img
            lbl.config(image=img)
            lbl.image = img  # جلوگیری از پاک شدن تصویر توسط garbage collector

    # --- ایجاد ۵ ستاره قابل کلیک ---
    for i in range(5):
        lbl = tk.Label(rating_frame, image=star_empty_img, bg="#f9f9f9", cursor="hand2")
        lbl.image = star_empty_img
        lbl.bind("<Button-1>", lambda e, r=i + 1: update_stars(r))
        lbl.pack(side="left", padx=2)
        star_labels.append(lbl)

    # --- نمایش متن امتیاز ---
    rating_value_label = tk.Label(bottom_wrapper, text="", font=("arial", 11), bg="#f9f9f9")
    rating_value_label.pack()

    def update_rating_label(*args):
        """
        متن نمایش داده شده در امتیاز را به‌روز می‌کند.
        """
        val = user_rating.get()
        rating_text = f"امتیاز: {convert_to_persian(val)} از {convert_to_persian(5)}"
        rating_value_label.config(text=rating_text)

    # اتصال تابع به تغییرات متغیر امتیاز
    user_rating.trace_add("write", update_rating_label)

    # --- نمایش اولیه ستاره‌ها و متن امتیاز ---
    update_stars(initial_rating)
    update_rating_label()

    # --- بخش نظرات کاربران ---
    # لیست کامنت‌های پیش‌فرض و کاربران
    all_comments = [
        "عالی بود، ممنون از اطلاعات خوبتون!",
        "محصول کیفیت خوبی داشت و به موقع ارسال شد.",
        "امیدوارم در آینده امکانات بیشتری اضافه بشه.",
        "کاش تخفیف بیشتری داشت.",
        "بسته‌بندی خیلی خوبی داشت، راضی بودم.",
        "پشتیبانی خیلی سریع پاسخ داد.",
        "کاملاً با عکس مطابقت داشت.",
        "ارسال با کمی تأخیر انجام شد ولی ارزشش رو داشت.",
        "کیفیت ساخت واقعا بالاست.",
        "برای بار دوم هم از این فروشگاه خرید کردم و راضی‌ام."
    ]

    # فقط آخرین ۳ کامنت برای نمایش اولیه
    comment_list = all_comments[-3:]

    # --- عنوان بخش نظرات ---
    tk.Label(bottom_wrapper, text="دیدگاه کاربران", font=("Tahoma", 12, "bold"),
             bg="dodgerblue", fg="white", width=25).pack(pady=(20, 15))

    # --- فریم نمایش کامنت‌ها ---
    comments_frame = tk.Frame(bottom_wrapper, bg="white", bd=1, relief="solid", width=240, height=120)
    comments_frame.pack(pady=(0, 10))
    comments_frame.pack_propagate(False)

    def show_comments():
        """
        آخرین ۳ کامنت را در فریم نمایش می‌دهد.
        """
        for widget in comments_frame.winfo_children():
            widget.destroy()

        # نمایش آخرین ۳ کامنت (جدیدترین در ابتدا)
        recent_comments = comment_list[-3:]
        for comment in reversed(recent_comments):
            lbl = tk.Label(
                comments_frame,
                text=f"{comment} •",
                font=("arial", 10),
                bg="white",
                anchor="e",
                justify="right",
                wraplength=220
            )
            lbl.pack(side="top", fill="x", padx=10, pady=2)

    # --- نمایش اولیه کامنت‌ها ---
    show_comments()

    # --- کادر ورودی برای نوشتن نظر جدید ---
    comment_input = tk.Text(bottom_wrapper, height=3, width=30, wrap="word", font=("arial", 10))
    comment_input.pack(pady=5)

    def submit_comment():
        """
        نظر وارد شده توسط کاربر را ذخیره و نمایش می‌کند.
        """
        c = comment_input.get("1.0", "end").strip()
        if c:
            save_comment(c)  # ذخیره در فایل
            comment_list.append(c)  # اضافه کردن به لیست فعلی
            comment_input.delete("1.0", "end")  # پاک کردن کادر ورودی
            show_comments()  # نمایش دوباره کامنت‌ها

    # --- دکمه ثبت نظر ---
    tk.Button(
        bottom_wrapper,
        text="ثبت نظر",
        font=("arial", 10, "bold"),
        bg="#64b5f6",
        fg="white",
        width=20,
        command=submit_comment
    ).pack(pady=(0, 10))

def load_products(category_name):
    """
    محصولات یک دسته‌بندی خاص را از فایل CSV مربوطه می‌خواند.
    اگر فایل وجود نداشت، لیست خالی برمی‌گرداند.
    """
    filename = f"{category_name}.csv"
    products = []

    try:
        with open(filename, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                name = row["name"]
                price = f"{int(row['price']):,}"  # قالب‌بندی قیمت با کاما
                image = f"image/{category_name}_{i+1}.png"  # مسیر تصویر بر اساس شماره
                products.append({
                    "name": name,
                    "price": price,
                    "image": image
                })
    except FileNotFoundError:
        print(f"⚠️ فایل {filename} یافت نشد")
    except Exception as e:
        print("خطا در خواندن فایل:", e)

    return products

def show_category_products(category_name):
    """
    پنجره‌ای جدید باز می‌کند و محصولات یک دسته‌بندی خاص را نمایش می‌دهد.
    شامل نوار بالا، جستجو و گرید محصولات است.
    """
    # ایجاد پنجره جدید برای دسته‌بندی
    window = tk.Toplevel()
    window.title(f"محصولات - {category_name}")
    window.geometry("1000x600+200+100")
    window.configure(bg=BG_COLOR)
    window.resizable(False, False)
    center_window(window, 1000, 600)

    # --- نوار بالایی ---
    nav_bar = tk.Frame(window, bg=THEME_COLOR, height=80)
    nav_bar.pack(fill="x", side="top")

    # لوگوی شرکت در سمت راست
    try:
        nav_logo = PhotoImage(file="shopera_nav_logo.png")
        logo_label = tk.Label(nav_bar, image=nav_logo, bg=THEME_COLOR)
        logo_label.image = nav_logo
    except:
        logo_label = tk.Label(nav_bar, text="Shopera", fg="white", bg=THEME_COLOR, font=("Arial", 18, "bold"))
    logo_label.pack(side="right", padx=10)

    # --- کادر جستجو ---
    search_frame = tk.Frame(nav_bar, bg="white", height=35)
    search_frame.pack(side="right", padx=10, pady=20)

    # ایجاد ورودی جستجو با قابلیت placeholder
    search_entry = tk.Entry(
        search_frame,
        font=("Arial", 12),
        fg="black",
        bg="white",
        relief="flat",           # حذف حاشیه مستطیل
        bd=0,                    # حذف کامل حاشیه
        highlightthickness=0,    # غیرفعال کردن خط دور
        justify="right"
    )
    search_entry.bind("<Button-1>", lambda e: search_entry.delete(0, tk.END))

    # اضافه کردن متن پیش‌فرض
    search_entry.insert(0, "جستجو...")

    # --- مدیریت متن پیش‌فرض (placeholder) ---
    def on_focus_in(event):
        """هنگام کلیک روی فیلد جستجو"""
        if search_entry.get() == "جستجو...":
            search_entry.delete(0, tk.END)
            search_entry.config(fg="black")

    def on_focus_out(event):
        """هنگام خروج از فیلد جستجو"""
        if search_entry.get() == "":
            search_entry.insert(0, "جستجو...")
            search_entry.config(fg="gray")

    # اتصال رویدادها به ورودی جستجو
    search_entry.bind("<FocusIn>", on_focus_in)
    search_entry.bind("<FocusOut>", on_focus_out)
    search_entry.pack(side="left", padx=(5, 0))

    # --- تابع انجام جستجو ---
    def perform_search():
        """جستجو بر اساس عبارت وارد شده و هدایت به دسته‌بندی مربوطه"""
        try:
            query = search_entry.get().strip()
            if query == "جستجو..." or not query:
                return

            # نقشه‌برداری از عبارات جستجو به دسته‌بندی‌ها
            category_mapping = {
                "موبایل": "موبایل",
                "موبايل": "موبایل",  # با ی عربی
                "گوشی": "موبایل",
                "گوشي": "موبایل",  # با ی عربی
                "mobile": "موبایل",
                "لپ تاپ": "لپ‌تاپ",
                "لپتاپ": "لپ‌تاپ",
                "لپ": "لپ‌تاپ",
                "هدفون": "هدفون",
                "هدست": "هدفون",
                "ساعت": "ساعت",
                "دیجیتال": "دیجیتال"
            }

            # نرمال‌سازی عبارت جستجو
            normalized_query = query.lower().replace(" ", "").replace("‌", "").replace("ي", "ی")

            # جستجو در نقشه‌برداری دسته‌بندی‌ها
            matched_category = None
            for key, value in category_mapping.items():
                normalized_key = key.lower().replace(" ", "").replace("‌", "").replace("ي", "ی")
                if normalized_query == normalized_key:
                    matched_category = value
                    break

            # بازگرداندن متن پیشفرض
            search_entry.delete(0, tk.END)
            search_entry.insert(0, "جستجو...")
            search_entry.config(fg="black")

            # نتیجه جستجو
            if matched_category:
                show_category_products(matched_category)
            else:
                messagebox.showinfo(
                    "نتیجه جستجو",
                    f"عبارت '{query}' یافت نشد\n\n"
                    "کلیدواژه‌های معتبر:\n"
                    "- موبایل\n- لپ‌تاپ\n- هدفون\n- ساعت\n- دیجیتال"
                )
            search_entry.delete(0, tk.END)
            search_entry.insert(0, "...جستجو")
        except Exception as e:
            messagebox.showerror("خطا", f"خطا در جستجو: {str(e)}")
            # در صورت خطا هم متن پیشفرض بازگردانده شود
            search_entry.delete(0, tk.END)
            search_entry.insert(0, "جستجو...")
            search_entry.config(fg="gray")

    # --- دکمه جستجو ---
    try:
        search_icon = PhotoImage(file="search_icon.png")
        search_btn = tk.Button(search_frame, image=search_icon, bg="white", bd=0, command=perform_search)
        search_btn.image = search_icon
    except:
        search_btn = tk.Button(search_frame, text="🔍", font=("Arial", 12), bg="white", bd=0, command=perform_search)
    search_btn.pack(side="right", padx=(0, 5))
    # --- فریم دکمه‌های سمت چپ نوار بالا ---
    buttons_frame = tk.Frame(nav_bar, bg=THEME_COLOR)
    buttons_frame.pack(side="left", padx=10)

    # --- دکمه بازگشت ---
    try:
        back_img = PhotoImage(file="backright.png").subsample(2, 2)
        back_btn = tk.Button(
            buttons_frame,
            image=back_img,
            bg=THEME_COLOR,  # رنگ پس‌زمینه دکمه
            activebackground=THEME_COLOR,  # رنگ هنگام کلیک
            bd=0,  # حذف حاشیه
            highlightthickness=0,  # حذف هایلایت
            relief="flat",  # حذف اثر سه بعدی
            command=window.destroy  # بستن پنجره فعلی
        )
        back_btn.image = back_img
    except:
        # اگر تصویر بارگذاری نشد، دکمه متنی نمایش داده شود
        back_btn = tk.Button(
            buttons_frame,
            text="بازگشت",
            font=("Arial", 11),
            bg=THEME_COLOR,
            fg="white",
            activebackground=THEME_COLOR,
            activeforeground="white",
            bd=0,
            highlightthickness=0,
            relief="flat",
            command=window.destroy
        )
    back_btn.pack(side="left", padx=5)

    # --- دکمه سبد خرید ---
    try:
        cart_img = PhotoImage(file="cart_icon.png")
        cart_btn = tk.Button(
            buttons_frame,
            image=cart_img,
            bg=THEME_COLOR,
            bd=0,
            command=show_cart_window  # باز کردن پنجره سبد خرید
        )
        cart_btn.image = cart_img
    except:
        # اگر تصویر بارگذاری نشد، آیکون یونیکد نمایش داده شود
        cart_btn = tk.Button(
            buttons_frame,
            text="🛒",
            font=("Arial", 14),
            bg=THEME_COLOR,
            fg="white",
            bd=0,
            command=show_cart_window
        )
    cart_btn.pack(side="left", padx=5)

    # --- عنوان دسته‌بندی ---
    category_label = tk.Label(
        window,
        text=category_name,
        font=("Arial", 20),
        fg=THEME_COLOR,
        bg=BG_COLOR
    )
    category_label.pack(anchor="ne", padx=137, pady=(5, 5))

    # --- فریم اصلی محصولات ---
    products_frame = tk.Frame(window, bg=BG_COLOR)
    products_frame.pack(pady=0)

    # --- بارگذاری محصولات ---
    products = load_products(category_name)

    # اگر محصولی از فایل بارگذاری نشد، داده‌های ساختگی ایجاد می‌شود
    if not products:
        for i in range(8):
            products.append({
                "name": f"{category_name} مدل {i + 1}",
                "price": f"{random.randint(5000000, 50000000):,}",
                "image": f"image/{category_name}_{i + 1}.png"
            })

    # --- نمایش ۸ محصول در شبکه 2x4 ---
    for idx, product in enumerate(products[:8]):
        # ایجاد فریم هر محصول
        frame = tk.Frame(products_frame, bg="white", bd=1, relief="solid", highlightbackground="gray",
                         highlightthickness=1)
        frame.grid(row=idx // 4, column=idx % 4, padx=5, pady=(0, 5))

        # --- افکت هاور (تغییر رنگ هنگام ماوس روی محصول) ---
        def on_enter(e, f=frame):
            f.config(bg="#f0f0f0")

        def on_leave(e, f=frame):
            f.config(bg="white")

        frame.bind("<Enter>", on_enter)
        frame.bind("<Leave>", on_leave)

        # --- نمایش تصویر محصول ---
        try:
            img = PhotoImage(file=product["image"])
            # تنظیم اندازه تصویر
            img = img.subsample(max(img.width() // 200, 1), max(img.height() // 200, 1))
            img_button = tk.Button(
                frame,
                image=img,
                command=lambda p=product: show_product_details(p),
                bg="white",
                bd=0,
                activebackground="white",
                cursor="hand2"
            )
            img_button.image = img
            img_button.pack(padx=10, pady=10)
        except:
            # اگر تصویر یافت نشد، آیکون خط قرمز نمایش داده شود
            tk.Button(
                frame,
                text="❌",
                command=lambda p=product: show_product_details(p),
                bg="white",
                fg="red",
                bd=0
            ).pack(padx=10, pady=10)

        # --- نام محصول ---
        tk.Label(
            frame,
            text=product["name"],
            font=("Arial", 11, "bold"),
            fg=THEME_COLOR,
            bg="white"
        ).pack(pady=(0, 3))

        # --- قیمت محصول ---
        tk.Label(
            frame,
            text=f"{product['price']} تومان",
            font=("Arial", 10),
            fg=THEME_COLOR,
            bg="white"
        ).pack()
def add_to_cart(product, selected_color):
    """
    محصول انتخاب شده را به سبد خرید اضافه می‌کند.
    اگر رنگی انتخاب نشده باشد، عملیات لغو می‌شود.
    """
    # اگر کاربر رنگی انتخاب نکرده باشد، افزودن لغو می‌شود
    if not selected_color:
        return

    # نقشه معکوس کدهای رنگ به نام فارسی
    reverse_color_map = {
        "#ffffff": "سفید",
        "#000000": "مشکی",
        "#9e9e9e": "طوسی",
        "#e53935": "قرمز",
        "#f5f5dc": "کرم"
    }

    # افزودن آیتم به سبد خرید
    cart_items.append({
        "name": product["name"],
        "image": product["image"],
        "price": product["price"],
        "color": reverse_color_map.get(selected_color, "رنگ نامشخص"),  # نام رنگ بر اساس کد
        "color_code": selected_color,  # کد رنگ برای نمایش دایره
        "qty": 1  # تعداد اولیه
    })

    # پیام موفقیت در کنسول
    print("✅ کالا به سبد خرید اضافه شد")


# --- متغیر جهانی برای مدیریت پنجره سبد خرید ---
# این متغیر آخرین پنجره سبد خرید باز شده را نگه می‌دارد
current_cart_window = None

# --- تابع اصلی: نمایش پنجره سبد خرید ---
def show_cart_window():
    """
    پنجره سبد خرید را باز می‌کند.
    اگر قبلاً باز بوده، آن را می‌بندد و یک پنجره جدید ایجاد می‌کند.
    """
    global current_cart_window

    # اگر پنجره سبد خرید قبلاً باز بوده، آن را می‌بندد تا از تکرار جلوگیری شود
    if current_cart_window is not None and current_cart_window.winfo_exists():
        current_cart_window.destroy()

    # ایجاد پنجره جدید سبد خرید
    cart_win = tk.Toplevel()
    current_cart_window = cart_win  # ذخیره مرجع پنجره فعلی

    # --- تنظیمات پایه پنجره ---
    cart_win.title("سبد خرید")
    cart_win.configure(bg="white")
    cart_win.resizable(False, False)
    center_window(cart_win, 1000, 600)  # وسط‌چین کردن پنجره

    # --- نوار ناوبری (Navigation Bar) ---
    nav_bar = tk.Frame(cart_win, bg=THEME_COLOR, height=80)
    nav_bar.pack(fill="x", side="top")

    # --- لوگو ---
    try:
        nav_logo = PhotoImage(file="shopera_nav_logo.png")
        logo_label = tk.Label(nav_bar, image=nav_logo, bg=THEME_COLOR)
        logo_label.image = nav_logo
    except:
        logo_label = tk.Label(nav_bar, text="Shopera", font=("Arial", 18, "bold"), fg="white", bg=THEME_COLOR)
    logo_label.pack(side="right", padx=10)

    # --- بخش جستجو ---
    search_frame = tk.Frame(nav_bar, bg="white", height=35)
    search_frame.pack(side="right", padx=10, pady=20)

    # --- کادر ورودی جستجو ---
    search_entry = tk.Entry(
        search_frame,
        font=("Arial", 12),
        fg="black",
        bg="white",
        relief="flat",  # حذف حاشیه مستطیل
        bd=0,  # حذف کامل حاشیه
        highlightthickness=0,  # غیرفعال کردن خط دور
        justify="right"  # تراز راست برای متن فارسی
    )
    search_entry.insert(0, "جستجو...")  # متن پیش‌فرض

    # --- مدیریت متن پیش‌فرض (placeholder) ---
    def on_focus_in(event):
        """هنگام کلیک روی فیلد جستجو"""
        if search_entry.get() == "جستجو...":
            search_entry.delete(0, tk.END)
            search_entry.config(fg="black")

    def on_focus_out(event):
        """هنگام خروج از فیلد جستجو"""
        if search_entry.get() == "":
            search_entry.insert(0, "جستجو...")
            search_entry.config(fg="gray")

    # اتصال رویدادهای فوکوس به ورودی جستجو
    search_entry.bind("<FocusIn>", on_focus_in)
    search_entry.bind("<FocusOut>", on_focus_out)
    search_entry.pack(side="left", padx=(5, 0))

    # --- تابع اجرای جستجو ---
    def perform_search():
        """
        جستجو بر اساس عبارت وارد شده و هدایت به دسته‌بندی مربوطه.
        از نرمال‌سازی و مقایسه دقیق استفاده می‌کند.
        """
        try:
            query = search_entry.get().strip()
            # اگر کاربر روی متن پیش‌فرض کلیک کرده یا فیلد خالی باشد
            if query == "جستجو..." or not query:
                return

            # نقشه‌برداری از کلمات کلیدی به دسته‌بندی‌ها
            category_mapping = {
                "موبایل": "موبایل",
                "موبايل": "موبایل",  # با ی عربی
                "گوشی": "موبایل",
                "گوشي": "موبایل",  # با ی عربی
                "mobile": "موبایل",
                "لپ تاپ": "لپ‌تاپ",
                "لپتاپ": "لپ‌تاپ",
                "لپ": "لپ‌تاپ",
                "هدفون": "هدفون",
                "هدست": "هدفون",
                "ساعت": "ساعت",
                "دیجیتال": "دیجیتال"
            }

            # نرمال‌سازی عبارت جستجو
            normalized_query = query.lower().replace(" ", "").replace("‌", "").replace("ي", "ی")

            # جستجو در نقشه‌برداری دسته‌بندی‌ها
            matched_category = None
            for key, value in category_mapping.items():
                normalized_key = key.lower().replace(" ", "").replace("‌", "").replace("ي", "ی")
                if normalized_query == normalized_key:
                    matched_category = value
                    break

            # بازنشانی کادر جستجو به حالت پیش‌فرض
            search_entry.delete(0, tk.END)
            search_entry.insert(0, "جستجو...")
            search_entry.config(fg="black")

            # نتیجه جستجو
            if matched_category:
                show_category_products(matched_category)
            else:
                messagebox.showinfo(
                    "نتیجه جستجو",
                    f"عبارت '{query}' یافت نشد\n\n"
                    "کلیدواژه‌های معتبر:\n"
                    "- موبایل\n- لپ‌تاپ\n- هدفون\n- ساعت\n- دیجیتال"
                )

            # تغییر موقت متن جستجو
            search_entry.delete(0, tk.END)
            search_entry.insert(0, "...جستجو")
        except Exception as e:
            messagebox.showerror("خطا", f"خطا در جستجو: {str(e)}")
            # بازگردانی متن پیش‌فرض در صورت خطا
            search_entry.delete(0, tk.END)
            search_entry.insert(0, "جستجو...")
            search_entry.config(fg="gray")

    # --- دکمه جستجو ---
    try:
        search_icon = PhotoImage(file="search_icon.png")
        search_btn = tk.Button(search_frame, image=search_icon, bg="white", bd=0, command=perform_search)
        search_btn.image = search_icon
    except:
        search_btn = tk.Button(search_frame, text="🔍", font=("Arial", 12), bg="white", bd=0, command=perform_search)
    search_btn.pack(side="right", padx=(0, 5))

    # --- فریم دکمه‌های سمت چپ (بازگشت و سبد خرید) ---
    buttons_frame = tk.Frame(nav_bar, bg=THEME_COLOR)
    buttons_frame.pack(side="left", padx=10)

    # --- دکمه بازگشت ---
    try:
        back_img = PhotoImage(file="backright.png").subsample(2, 2)
        back_btn = tk.Button(
            buttons_frame,
            image=back_img,
            bg=THEME_COLOR,  # رنگ پس‌زمینه دکمه
            activebackground=THEME_COLOR,  # رنگ هنگام کلیک
            bd=0,  # حذف حاشیه
            highlightthickness=0,  # حذف هایلایت
            relief="flat",  # حذف اثر سه بعدی
            command=cart_win.destroy  # بستن پنجره سبد خرید
        )
        back_btn.image = back_img
    except:
        # اگر تصویر بارگذاری نشد، دکمه متنی نمایش داده شود
        back_btn = tk.Button(
            buttons_frame,
            text="بازگشت",
            font=("Arial", 11),
            bg=THEME_COLOR,
            fg="white",
            activebackground=THEME_COLOR,
            activeforeground="white",
            bd=0,
            highlightthickness=0,
            relief="flat",
            command=cart_win.destroy
        )
    back_btn.pack(side="left", padx=5)

    # --- دکمه سبد خرید ---
    try:
        cart_img = PhotoImage(file="cart_icon.png")
        cart_btn = tk.Button(
            buttons_frame,
            image=cart_img,
            bg=THEME_COLOR,
            bd=0,
            command=show_cart_window  # باز کردن پنجره سبد خرید
        )
        cart_btn.image = cart_img
    except:
        # اگر تصویر بارگذاری نشد، آیکون یونیکد نمایش داده شود
        cart_btn = tk.Button(
            buttons_frame,
            text="🛒",
            font=("Arial", 14),
            bg=THEME_COLOR,
            fg="white",
            bd=0,
            command=show_cart_window
        )
    cart_btn.pack(side="left", padx=5)

    # --- عنوان اصلی سبد خرید ---
    tk.Label(cart_win, text="سبد خرید شما", font=("Arial", 18, "bold"),
             fg=THEME_COLOR, bg="white").pack(anchor="ne", padx=42, pady=(15, 10))

    # --- کانتینر اصلی محتوا ---
    main_container = tk.Frame(cart_win, bg="white")
    main_container.pack(fill="both", expand=True)

    # --- حالت سبد خالی ---
    if not cart_items:
        try:
            # نمایش تصویر سبد خالی
            empty_img = PhotoImage(file="empty_cart.png")
            img_label = tk.Label(main_container, image=empty_img, bg="white")
            img_label.image = empty_img
            img_label.pack(pady=(50, 10))
        except:
            pass  # اگر تصویر وجود نداشت، بدون خطا ادامه بده

        # پیام سبد خالی
        tk.Label(main_container, text=".چیزی برای نمایش موجود نیست", font=("Arial", 17),
                 fg="#3ca5c1", bg="white").pack()
        return  # خروج از تابع در صورت خالی بودن سبد

    # --- حالت سبد دارای محصول ---
    # بارگذاری آیکون‌های افزایش و حذف
    try:
        plus_img = tk.PhotoImage(file="sabad/plus.png").subsample(1, 1)  # آیکون افزایش تعداد
        bin_img = tk.PhotoImage(file="sabad/bin.png").subsample(1, 1)  # آیکون حذف
    except:
        plus_img = None
        bin_img = None

    # --- محاسبه تعداد کل آیتم‌ها ---
    total_items = sum(item['qty'] for item in cart_items)

    # --- پنل سمت چپ (اطلاعات پرداخت) ---
    left_frame = tk.Frame(main_container, bg="white", bd=0, relief="solid", width=280, height=1,
                          highlightthickness=1, highlightbackground="#dddddd")
    left_frame.pack(side="left", fill="y", padx=(60, 15), pady=(20, 212), anchor="n")
    left_frame.pack_propagate(False)  # جلوگیری از تغییر اندازه فریم

    # --- فریم محتوای محصولات ---
    content_frame = tk.Frame(main_container, bg="white")
    content_frame.pack(side="right", fill="both", expand=True, padx=20, pady=10)

    # --- محاسبه جمع کل قیمت ---
    total_price = 0  # متغیر برای ذخیره جمع کل قیمت

    # --- حلقه ایجاد محصولات در سبد خرید ---
    for index, item in enumerate(cart_items):
        # --- فریم هر محصول ---
        product_frame = tk.Frame(content_frame, bg="white", width=650, height=250, bd=0,
                                 highlightbackground="#dddddd", highlightthickness=1, relief="flat")
        product_frame.pack(fill="x", padx=20, pady=10)
        product_frame.pack_propagate(False)  # جلوگیری از تغییر اندازه فریم

        # --- سمت راست: تصویر محصول ---
        right_side = tk.Frame(product_frame, bg="white")
        right_side.pack(side="right", padx=20, pady=10)

        try:
            # نمایش تصویر محصول
            img = PhotoImage(file=item["image"]).subsample(1, 1)
            img_label = tk.Label(right_side, image=img, bg="white")
            img_label.image = img
            img_label.pack(pady=(0, 9))
        except:
            # اگر تصویر یافت نشد، متن "تصویر محصول" نمایش داده شود
            img_label = tk.Label(right_side, text="تصویر محصول", font=("Arial", 10), bg="white")
            img_label.pack(pady=(0, 10))

        # --- کانتینر کنترل‌های مقدار (افزایش، کاهش، حذف) ---
        controls_container = tk.Frame(right_side, bg="white", bd=0, relief="solid", width=80, height=70,
                                      highlightbackground="lightblue", highlightthickness=1)
        controls_container.pack()

        controls_frame = tk.Frame(controls_container, bg="white")
        controls_frame.pack(padx=3, pady=3)

        # --- دکمه افزایش تعداد ---
        if plus_img:
            plus_btn = tk.Button(controls_frame, image=plus_img,
                                 command=lambda idx=index: increase_qty(idx),
                                 bd=0, bg="white", activebackground="white")
            plus_btn.image = plus_img
        else:
            plus_btn = tk.Button(controls_frame, text="+",
                                 command=lambda idx=index: increase_qty(idx),
                                 font=("Arial", 10), bd=1, bg="white")
        plus_btn.pack(side="right", padx=5)

        # --- نمایش تعداد فعلی ---
        qty_label = tk.Label(controls_frame, text=str(item["qty"]),
                             font=("Arial", 12, "bold"),
                             fg="#19a5ea", bg="white", width=3)
        qty_label.pack(side="right", padx=5)

        # --- دکمه کاهش/حذف ---
        if bin_img:
            bin_btn = tk.Button(controls_frame, image=bin_img,
                                command=lambda idx=index: decrease_qty(idx),
                                bd=0, bg="white", activebackground="white")
            bin_btn.image = bin_img
        else:
            bin_btn = tk.Button(controls_frame, text="حذف",
                                command=lambda idx=index: decrease_qty(idx),
                                font=("Arial", 10), bd=1, bg="white")
        bin_btn.pack(side="right", padx=5)

        # --- سمت چپ: جزئیات محصول ---
        detail_frame = tk.Frame(product_frame, bg="white")
        detail_frame.pack(side="right", fill="both", expand=True, padx=20, pady=15)

        # --- نام محصول ---
        tk.Label(detail_frame, text=item["name"],
                 font=("Arial", 16, "bold"), bg="white").pack(anchor="e", pady=(0, 10))

        # --- رنگ انتخابی ---
        tk.Label(detail_frame, text=f"رنگ انتخابی: {item['color']}",
                 font=("Arial", 12), bg="white").pack(anchor="e", pady=(0, 15))

        # --- نمایش رنگ به صورت دایره ---
        color_canvas = tk.Canvas(detail_frame, width=24, height=24, bg="white", highlightthickness=0)
        color_canvas.pack(anchor="e", pady=(0, 15))
        color_canvas.create_oval(2, 2, 22, 22,
                                 fill=item["color_code"],
                                 outline="black",
                                 width=1)

        # --- گارانتی ---
        tk.Label(detail_frame, text="ضمانت گارانتی",
                 font=("Arial", 14), fg="gray", bg="white").pack(anchor="e", pady=(0, 10))

        # --- قیمت ---
        price_frame = tk.Frame(detail_frame, bg="white")
        price_frame.pack(anchor="e", pady=(8, 0))

        # بررسی اینکه آیا کالا یکی از ۵ کالای تخفیفی است
        product_name = item["name"]
        discount_data = DISCOUNTED_PRODUCTS.get(product_name)

        if discount_data:
            # حذف کاما و تبدیل به عدد برای مقایسه
            try:
                item_price_clean = int(item["price"].replace(",", ""))
                original_price_clean = int(discount_data["original"].replace(",", ""))
                if item_price_clean == original_price_clean:
                    # قیمت اصلی (خط‌خورده و خاکستری)
                    tk.Label(
                        detail_frame,
                        text=f"قیمت: {discount_data['original']} تومان",
                        font=("Arial", 12),
                        bg="white",
                        fg="lightgray"
                    ).pack(anchor="e", pady=(0, 2))
                    # قیمت تخفیف‌خورده (قرمز و بولد)
                    tk.Label(
                        detail_frame,
                        text=f"قیمت ویژه: {discount_data['discounted']} تومان",
                        font=("Arial", 13, "bold"),
                        bg="white",
                        fg="red"
                    ).pack(anchor="e")
                    final_price = int(discount_data["discounted"].replace(",", ""))
                else:
                    # اگر قیمت با اصلی مطابقت نداشت (مثلاً از قبل تخفیف خورده بوده)
                    tk.Label(
                        detail_frame,
                        text=f"قیمت: {item['price']} تومان",
                        font=("Arial", 15, "bold"),
                        bg="white",
                        fg="black"
                    ).pack(anchor="e", pady=(8, 0))
                    final_price = item_price_clean
            except:
                # اگر تبدیل عددی خطا داد
                tk.Label(
                    detail_frame,
                    text=f"قیمت: {item['price']} تومان",
                    font=("Arial", 15, "bold"),
                    bg="white",
                    fg="black"
                ).pack(anchor="e", pady=(8, 0))
                final_price = 0
        else:
            # اگر کالا تخفیف نداشت
            tk.Label(
                detail_frame,
                text=f"قیمت: {item['price']} تومان",
                font=("Arial", 15, "bold"),
                bg="white",
                fg="black"
            ).pack(anchor="e", pady=(8, 0))
            final_price = int(item["price"].replace(",", ""))

        # --- محاسبه جمع کل با قیمت واقعی (تخفیف‌خورده یا عادی) ---
        total_price += final_price * item["qty"]

# # پنل پرداخت سمت چپ
    # --------------------------------------------
    # نمایش تعداد کالاها
    tk.Label(left_frame,
             text=f"تعداد کالا: {total_items} عدد",
             font=("Arial", 14),
             bg="white"
             ).pack(pady=(40, 10))

    # نمایش جمع کل
    tk.Label(left_frame,
             text=f"جمع کل: {total_price:,} تومان",
             font=("Arial", 15),
             bg="white"
             ).pack(pady=0)

    # دکمه تأیید نهایی
    def confirm_order():
        if not current_user:
            messagebox.showerror("خطا", "کاربری وارد نشده است.")
            return
        for item in cart_items:

            product_id = f"{item['name']}_{item['color']}"  # یا از داده واقعی بگیر
            save_order_to_csv(
                username=current_user["username"],  # فرض می‌کنیم current_user دارای username باشه
                product_id=product_id,
                quantity=item["qty"],
                total_price=int(item["price"].replace(",", "")) * item["qty"],
                date=datetime.now().strftime("%Y/%m/%d %H:%M")
            )
        # پاک کردن سبد خرید بعد از ثبت
        cart_items.clear()
        messagebox.showinfo("موفقیت", "سفارش شما با موفقیت ثبت شد!")
        cart_win.destroy()  #  بستن پنجره سبد خرید


    tk.Button(left_frame, text="تأیید و تکمیل سفارش", bg="#19a5ea", fg="white", font=("Arial", 15, "bold"),
              width=18, height=1, command=confirm_order).pack(pady=(60, 10))


# --------------------------------------------
# توابع مدیریت مقدار محصولات
# --------------------------------------------
def increase_qty(index):
    """افزایش تعداد آیتم در سبد خرید"""
    cart_items[index]["qty"] += 1
    show_cart_window()  # بازسازی پنجره برای به‌روزرسانی


def decrease_qty(index):
    """کاهش یا حذف آیتم از سبد خرید"""
    if cart_items[index]["qty"] > 1:
        cart_items[index]["qty"] -= 1  # کاهش تعداد
    else:
        del cart_items[index]  # حذف کامل محصول
    show_cart_window()  # بازسازی پنجره
#  -------ادمین -----
def show_admin_panel():
    win = tk.Toplevel()
    win.title("پنل مدیریت")
    center_window(win, 1000, 600)
    win.configure(bg="white")
    win.resizable(False, False)

    # نوار بالا و لوگو
    nav_bar = tk.Frame(win, bg=THEME_COLOR, height=80)
    nav_bar.pack(fill="x", side="top")
    try:
        nav_logo = PhotoImage(file="shopera_nav_logo.png")
        logo_label = tk.Label(nav_bar, image=nav_logo, bg=THEME_COLOR)
        logo_label.image = nav_logo
    except:
        logo_label = tk.Label(nav_bar, text="Shopera", font=("Arial", 18, "bold"), fg="white", bg=THEME_COLOR)
    logo_label.pack(side="right", padx=10)

    tk.Label(win, text="پنل مدیریت", font=("Arial", 20, "bold"), fg=THEME_COLOR, bg="white").pack(pady=20)

    # فریم مرکزی برای کارت‌ها
    cards_frame = tk.Frame(win, bg="white")
    cards_frame.pack(pady=20)

    # تابع ساخت کارت یکدست
    def create_admin_card(parent, text, icon, command):
        card = tk.Frame(parent, bg="#bbdefb", bd=1, relief="solid", width=200, height=200)
        card.pack(side="left", padx=20, pady=10)
        card.pack_propagate(False)

        try:
            img = PhotoImage(file=f"{icon}.png").subsample(2, 2)
            img_label = tk.Label(card, image=img, bg="#bbdefb")  # پس‌زمینه = رنگ کارت
            img_label.image = img
            img_label.pack(pady=10)
        except:
            tk.Label(card, text=icon, font=("Arial", 24), bg="#bbdefb").pack(pady=10)

        tk.Label(card, text=text, font=("Arial", 14, "bold"), bg="#bbdefb").pack()

        # هاور افکت
        def on_enter(e):
            card.config(bg="#e3f2fd")  # وقتی ماوس روی کارت باشه، کمرنگ‌تر بشه
        def on_leave(e):
            card.config(bg="#bbdefb")
        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)
        for child in card.winfo_children():
            child.bind("<Enter>", on_enter)
            child.bind("<Leave>", on_leave)
            child.bind("<Button-1>", lambda e: command())

    # ساخت سه کارت با یک رنگ (رنگ وسطی آبی)
    create_admin_card(cards_frame, "مدیریت کالاها", "manage_products", manage_products)
    create_admin_card(cards_frame, "گزارش فروش", "sales_report", show_sales_report)
    create_admin_card(cards_frame, "مشاهده سفارشات", "view_orders", show_orders)

    # دکمه بستن
    tk.Button(win, text=" بستن", font=("Arial", 12), fg="white", bg=THEME_COLOR, width=20,
              command=win.destroy).pack(pady=30)
# مدیریت کالا ها
from datetime import datetime
from tkinter import ttk, messagebox, filedialog, PhotoImage

# تابع مرکزی مدیریت کالاها
def manage_products():
    win = tk.Toplevel()
    win.title(" مدیریت کالاها")
    center_window(win, 1000, 600)
    win.configure(bg="white")
    win.resizable(False, False)

    # --- متغیرها ---
    products = []
    original_products = []

    # --- تابع بارگذاری محصولات ---
    def load_products_from_csv():
        nonlocal products, original_products
        try:
            with open('products.csv', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                products = []
                for row in reader:
                    if 'created_at' not in row:
                        row['created_at'] = datetime.now().strftime("%Y-%m-%d %H:%M")
                    if 'updated_at' not in row:
                        row['updated_at'] = row['created_at']
                    products.append(row)
                original_products = products.copy()
        except FileNotFoundError:
            error_label = tk.Label(win, text="⚠ فایل products.csv یافت نشد!", font=("Arial", 10, "bold"), fg="red", bg="white")
            error_label.pack(pady=5)
            win.after(3000, error_label.destroy)
        except Exception as e:
            error_label = tk.Label(win, text=f"⚠ خطای خواندن فایل: {e}", font=("Arial", 10, "bold"), fg="red", bg="white")
            error_label.pack(pady=5)
            win.after(3000, error_label.destroy)
        refresh_table()

    # --- تابع ذخیره ---
    def save_products_to_csv():
        try:
            with open('products.csv', 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=[
                    "product_id", "name", "price", "stock", "category", "image", "created_at", "updated_at"
                ])
                writer.writeheader()
                writer.writerows(products)
        except Exception as e:
            error_label = tk.Label(win, text=f"⚠ ذخیره ناموفق: {e}", font=("Arial", 10, "bold"), fg="red", bg="white")
            error_label.pack(pady=5)
            win.after(3000, error_label.destroy)

    # --- تابع فیلتر ---
    def apply_filters():
        filtered = original_products
        cat = category_var.get()
        query = search_var.get().strip().lower()
        if cat != "همه":
            filtered = [p for p in filtered if p["category"] == cat]
        if query and query != "جستجو...":
            filtered = [p for p in filtered if query in p["name"].lower() or query in p["product_id"].lower()]
        products[:] = filtered
        refresh_table()

    # --- نوار بالایی ---
    nav_bar = tk.Frame(win, bg=THEME_COLOR, height=80)
    nav_bar.pack(side="top", fill="x")

    # 1. لوگو (راست‌ترین عنصر)
    try:
        nav_logo = PhotoImage(file="shopera_nav_logo.png")
        logo_label = tk.Label(nav_bar, image=nav_logo, bg=THEME_COLOR)
        logo_label.image = nav_logo
    except:
        logo_label = tk.Label(nav_bar, text="Shopera", font=("Arial", 16, "bold"), fg="white", bg=THEME_COLOR)
    logo_label.pack(side="right", padx=10)

    # 2. کادر جستجو
    search_frame = tk.Frame(nav_bar, bg="white", height=35)
    search_frame.pack(side="right", padx=10, pady=20)
    search_var = tk.StringVar()
    search_entry = tk.Entry(
        search_frame,
        textvariable=search_var,
        font=("Arial", 12),
        fg="gray",
        bg="white",
        relief="flat",
        bd=0,
        highlightthickness=0,
        justify="right",
        width=25
    )
    search_entry.insert(0, "...جستجو")
    search_entry.pack(side="left", padx=(5, 0))

    def on_focus_in(event):
        if search_entry.get() == "...جستجو":
            search_entry.delete(0, tk.END)
            search_entry.config(fg="black")

    def on_focus_out(event):
        if search_entry.get() == "":
            search_entry.insert(0, "جستجو...")
            search_entry.config(fg="gray")

    search_entry.bind("<FocusIn>", on_focus_in)
    search_entry.bind("<FocusOut>", on_focus_out)

    try:
        search_icon = PhotoImage(file="search_icon.png")
        search_btn = tk.Button(search_frame, image=search_icon, bg="white", bd=0, command=apply_filters)
        search_btn.image = search_icon
    except:
        search_btn = tk.Button(search_frame, text="🔍", font=("Arial", 12), bg="white", bd=0, command=apply_filters)
    search_btn.pack(side="right", padx=(0, 5))

    # 3. گروه چپ: شامل دکمه بازگشت، افزودن و فیلتر
    left_group = tk.Frame(nav_bar, bg=THEME_COLOR)
    left_group.pack(side="left", padx=10)

    # دکمه بازگشت
    try:
        back_img = PhotoImage(file="backright.png").subsample(2, 2)
        back_btn = tk.Button(
            left_group,
            image=back_img,
            bg=THEME_COLOR,
            bd=0,
            command=win.destroy
        )
        back_btn.image = back_img
    except:
        back_btn = tk.Button(
            left_group,
            text="بازگشت",
            font=("Arial", 11),
            bg=THEME_COLOR,
            fg="white",
            bd=0,
            command=win.destroy
        )
    back_btn.pack(side="left", padx=5)

    # دکمه افزودن کالا
    add_btn = tk.Button(
        left_group,
        text="➕ افزودن کالا",
        bg="white",
        fg=THEME_COLOR,
        font=("Arial", 11, "bold"),
        command=lambda: open_add_product_window()
    )
    add_btn.pack(side="left", padx=(10, 5))

    # فیلتر دسته‌بندی (کنار دکمه افزودن)
    filter_frame = tk.Frame(left_group, bg="white", height=35)
    filter_frame.pack(side="left", padx=(0, 0), pady=20)
    tk.Label(filter_frame, text="|", bg="white", fg="gray").pack(side="left", padx=(0, 5))
    category_var = tk.StringVar(value="همه")
    category_combo = ttk.Combobox(
        filter_frame,
        textvariable=category_var,
        values=["همه", "موبایل", "لپ‌تاپ", "هدفون", "ساعت", "دیجیتال"],
        width=10,
        font=("Arial", 11)
    )
    category_combo.pack(side="left")
    category_combo.bind("<<ComboboxSelected>>", lambda e: apply_filters())

    # --- عنوان صفحه ---
    tk.Label(win, text=" مدیریت کالاها", font=("Arial", 18, "bold"), fg=THEME_COLOR, bg="white").pack(pady=(10, 5))

    # --- فریم مرکزی ---
    main_frame = tk.Frame(win, bg="white")
    main_frame.pack(fill="both", expand=True, padx=20, pady=10)

    # --- جدول ---
    columns = ("product_id", "name", "price", "stock", "category", "created_at")
    tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=10)
    tree.pack(fill="both", expand=True)

    for col in columns:
        tree.heading(col, text={"product_id": "شناسه", "name": "نام کالا", "price": "قیمت", "stock": "موجودی", "category": "دسته", "created_at": "تاریخ ایجاد"}[col])
        tree.column(col, width={"product_id": 100, "name": 180, "price": 110, "stock": 90, "category": 100, "created_at": 130}[col], anchor="center")

    style = ttk.Style()
    style.configure("Treeview", rowheight=30, font=("Arial", 12))
    style.configure("Treeview.Heading", font=("Arial", 11, "bold"), foreground=THEME_COLOR)

    tree.tag_configure("hover", background="#f0f8ff")
    def on_hover(event):
        item = tree.identify_row(event.y)
        for i in tree.get_children():
            tree.item(i, tags=())
        if item:
            tree.item(item, tags=("hover",))
    tree.bind("<Motion>", on_hover)

    # --- تابع بازسازی جدول ---
    def refresh_table():
        for row in tree.get_children():
            tree.delete(row)
        for p in products:
            tree.insert("", "end", values=(
                p["product_id"],
                p["name"],
                f"{int(p['price']):,}",
                p["stock"],
                p["category"],
                p["created_at"]
            ))

    # --- توابع مدیریت ---

    def open_add_product_window():
        edit_win = tk.Toplevel(win)
        edit_win.title("➕ افزودن کالا جدید")
        center_window(edit_win, 1000, 600)
        edit_win.configure(bg="white")
        edit_win.resizable(False, False)

        # --- نوار بالایی ---
        nav_bar_edit = tk.Frame(edit_win, bg=THEME_COLOR, height=80)
        nav_bar_edit.pack(side="top", fill="x")
        try:
            nav_logo = PhotoImage(file="shopera_nav_logo.png")
            logo_label = tk.Label(nav_bar_edit, image=nav_logo, bg=THEME_COLOR)
            logo_label.image = nav_logo
        except:
            logo_label = tk.Label(nav_bar_edit, text="Shopera", font=("Arial", 16, "bold"), fg="white", bg=THEME_COLOR)
        logo_label.pack(side="right", padx=10)

        # --- دکمه بازگشت ---
        back_frame = tk.Frame(nav_bar_edit, bg=THEME_COLOR)
        back_frame.pack(side="left", padx=10)
        try:
            back_img = PhotoImage(file="backright.png").subsample(2, 2)
            back_btn = tk.Button(back_frame, image=back_img, bg=THEME_COLOR, bd=0, command=edit_win.destroy)
            back_btn.image = back_img
        except:
            back_btn = tk.Button(back_frame, text="بازگشت", font=("Arial", 11), bg=THEME_COLOR, fg="white", bd=0, command=edit_win.destroy)
        back_btn.pack(side="left", padx=5)

        # --- فرم ورودی ---
        form_frame = tk.Frame(edit_win, bg="white")
        form_frame.pack(pady=30, padx=30, fill="both", expand=True)

        fields = {
            "product_id": tk.StringVar(),
            "name": tk.StringVar(),
            "price": tk.StringVar(),
            "stock": tk.StringVar(),
            "category": tk.StringVar(value="موبایل"),
            "image": tk.StringVar()
        }
        labels = {
            "product_id": ":شناسه کالا",
            "name": ":نام کالا",
            "price": ":قیمت",
            "stock": ":موجودی",
            "category": ":دسته",
            "image": ":مسیر تصویر"
        }

        for key, label_text in labels.items():
            row = tk.Frame(form_frame, bg="white")
            row.pack(fill="x", pady=8)
            label = tk.Label(
                row,
                text=f"{label_text}",
                font=("Arial", 12, "bold"),
                bg="white",
                width=14,
                anchor="e"
            )
            label.pack(side="right", padx=(0, 10))

            if key == "category":
                cb = ttk.Combobox(row, textvariable=fields[key], values=("موبایل", "لپ‌تاپ", "هدفون", "ساعت", "دیجیتال"), state="readonly", font=("Arial", 11))
                cb.pack(side="right", ipady=2, ipadx=20, padx=(0, 15))
            elif key == "image":
                entry = tk.Entry(row, textvariable=fields[key], font=("Arial", 10), bg="white", fg="black", bd=1, relief="solid", width=20)
                entry.pack(side="right", ipady=2, ipadx=20, padx=(0, 15))
                def browse():
                    path = filedialog.askopenfilename(title="انتخاب تصویر محصول", filetypes=[("Image files", "*.png *.jpg *.jpeg")])
                    if path:
                        fields["image"].set(path)
                tk.Button(row, text="🔍", command=browse, bg="lightgray", width=3).pack(side="right")
            else:
                entry = tk.Entry(row, textvariable=fields[key], font=("Arial", 10), bg="white", fg="black", bd=1, relief="solid", width=20)
                entry.pack(side="right", ipady=2, ipadx=20, padx=(0, 15))

        # --- نمایش خطا ---
        error_label = tk.Label(
            edit_win,
            text="",
            font=("Arial", 11, "bold"),
            fg="red",
            bg="white",
            wraplength=900,
            justify="right"
        )
        error_label.pack(pady=5)

        def save():
            data = {k: v.get().strip() for k, v in fields.items()}
            if not all(data.values()):
                error_label.config(text=".لطفاً همه فیلدها را پر کنید")
                return
            try:
                int(data["price"])
                int(data["stock"])
            except:
                error_label.config(text=".قیمت و موجودی باید عدد باشند")
                return
            error_label.config(text="")  # پاک کردن خطا
            data["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
            data["updated_at"] = data["created_at"]
            products.append(data)
            original_products.append(data)
            save_products_to_csv()
            refresh_table()
            edit_win.destroy()

        tk.Button(
            edit_win,
            text=" ذخیره کالا",
            bg=THEME_COLOR,
            fg="white",
            font=("Arial", 14, "bold"),
            width=20,
            height=2,
            command=save
        ).pack(pady=40)

    def delete_product():
        selected = tree.selection()
        if not selected:
            error_label.config(text=" .لطفاً یک کالا را انتخاب کنید")
            win.after(3000, lambda: error_label.config(text=""))
            win.after(3000, lambda: error_label.config(text=""))
            return
        item = tree.item(selected[0])
        product_id = item['values'][0]
        confirm = messagebox.askyesno("تأیید", f"آیا از حذف کالا با شناسه {product_id} مطمئن هستید؟")
        if confirm:
            global products, original_products
            products = [p for p in products if p["product_id"] != product_id]
            original_products = [p for p in original_products if p["product_id"] != product_id]
            save_products_to_csv()
            refresh_table()
            error_label.config(text="✅ کالا با موفقیت حذف شد.")
            win.after(3000, lambda: error_label.config(text=""))

    def edit_product():
        nonlocal error_label
        selected = tree.selection()
        if not selected:
            error_label.config(text=" .لطفاً یک کالا را انتخاب کنید")
            win.after(3000, lambda: error_label.config(text=""))
            win.after(3000, lambda: error_label.config(text=""))
            return
        item = tree.item(selected[0])
        product_id = item['values'][0]
        product = next((p for p in products if p["product_id"] == product_id), None)
        if not product:
            error_label.config(text="❌ محصول مورد نظر یافت نشد.")
            win.after(3000, lambda: error_label.config(text=""))
            return

        # ---ویرایش ---
        edit_win = tk.Toplevel(win)
        edit_win.title(" ویرایش کالا")
        center_window(edit_win, 1000, 600)
        edit_win.configure(bg="white")
        edit_win.resizable(False, False)

        # --- نوار بالایی ---
        nav_bar_edit = tk.Frame(edit_win, bg=THEME_COLOR, height=80)
        nav_bar_edit.pack(side="top", fill="x")
        try:
            nav_logo = PhotoImage(file="shopera_nav_logo.png")
            logo_label = tk.Label(nav_bar_edit, image=nav_logo, bg=THEME_COLOR)
            logo_label.image = nav_logo
        except:
            logo_label = tk.Label(nav_bar_edit, text="Shopera", font=("Arial", 16, "bold"), fg="white", bg=THEME_COLOR)
        logo_label.pack(side="right", padx=10)

        back_frame = tk.Frame(nav_bar_edit, bg=THEME_COLOR)
        back_frame.pack(side="left", padx=10)
        try:
            back_img = PhotoImage(file="backright.png").subsample(2, 2)
            back_btn = tk.Button(back_frame, image=back_img, bg=THEME_COLOR, bd=0, command=edit_win.destroy)
            back_btn.image = back_img
        except:
            back_btn = tk.Button(back_frame, text="بازگشت", font=("Arial", 11), bg=THEME_COLOR, fg="white", bd=0,
                                 command=edit_win.destroy)
        back_btn.pack(side="left", padx=5)

        # --- فرم ویرایش ---
        form_frame = tk.Frame(edit_win, bg="white")
        form_frame.pack(pady=30, padx=30, fill="both", expand=True)

        combined_frame = tk.Frame(form_frame, bg="white")
        combined_frame.pack(fill="x", expand=True)

        left_form = tk.Frame(combined_frame, bg="white", width=600)
        left_form.pack(side="right", fill="y", padx=(0, 20))
        left_form.pack_propagate(False)

        fields = {
            "product_id": tk.StringVar(value=product["product_id"]),
            "name": tk.StringVar(value=product["name"]),
            "price": tk.StringVar(value=product["price"]),
            "stock": tk.StringVar(value=product["stock"]),
            "category": tk.StringVar(value=product["category"]),
            "image": tk.StringVar(value=product.get("image", ""))
        }

        labels = {
            "product_id": "شناسه کالا",
            "name": "نام کالا",
            "price": "قیمت (تومان)",
            "stock": "موجودی",
            "category": "دسته",
            "image": "مسیر تصویر"
        }

        for key, label_text in labels.items():
            row = tk.Frame(left_form, bg="white")
            row.pack(fill="x", pady=8)

            lbl = tk.Label(row, text=f"\u200F{label_text}:", font=("Arial", 12, "bold"), bg="white", width=14,
                           anchor="e")
            lbl.pack(side="right", padx=(0, 10))

            if key == "category":
                cb = ttk.Combobox(row, textvariable=fields[key],
                                  values=("موبایل", "لپ‌تاپ", "هدفون", "ساعت", "دیجیتال"), state="readonly",
                                  font=("Arial", 11))
                cb.pack(side="right", ipady=2, ipadx=20, padx=(0, 15))
            elif key == "image":
                entry = tk.Entry(row, textvariable=fields[key], font=("Arial", 10), bg="white", fg="black", bd=1,
                                 relief="solid", width=20)
                entry.pack(side="right", ipady=2, ipadx=20, padx=(0, 15))

                def browse():
                    path = filedialog.askopenfilename(title="انتخاب تصویر محصول",
                                                      filetypes=[("Image files", "*.png *.jpg *.jpeg")])
                    if path:
                        fields["image"].set(path)

                tk.Button(row, text="🔍", command=browse, bg="lightgray", width=3).pack(side="right")
            else:
                entry = tk.Entry(row, textvariable=fields[key], font=("Arial", 10), bg="white", fg="black", bd=1,
                                 relief="solid", width=20)
                entry.pack(side="right", ipady=2, ipadx=20, padx=(0, 15))

        # --- فریم دکمه ذخیره ---
        save_btn_frame = tk.Frame(combined_frame, bg="white", width=300)
        save_btn_frame.pack(side="left", fill="y", padx=(20, 0))
        save_btn_frame.pack_propagate(False)

        # --- نمایش خطا در پنجره ویرایش ---
        edit_error_label = tk.Label(
            save_btn_frame,
            text="",
            font=("Arial", 11),
            fg="red",
            bg="white",
            wraplength=250,
            justify="right"
        )
        edit_error_label.pack(pady=(10, 5))

        def save():
            data = {k: v.get().strip() for k, v in fields.items()}
            if not all(data.values()):
                edit_error_label.config(text="⚠ لطفاً همه فیلدها را پر کنید.")
                return
            try:
                int(data["price"])
                int(data["stock"])
            except:
                edit_error_label.config(text="⚠ قیمت و موجودی باید عدد باشند.")
                return

            edit_error_label.config(text="")  # پاک کردن خطا
            product.update(data)
            product["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
            save_products_to_csv()
            refresh_table()
            edit_win.destroy()
            # نمایش موفقیت در صفحه اصلی
            error_label.config(text="✅ تغییرات ذخیره شد.")
            win.after(3000, lambda: error_label.config(text=""))

        tk.Button(save_btn_frame, text="✅ ذخیره تغییرات", bg="#2196F3", fg="white", font=("Arial", 11, "bold"),
                  width=20, height=2,
                  command=save).pack(pady=5)
        # --- فرم ویرایش ---
        form_frame = tk.Frame(edit_win, bg="white")
        form_frame.pack(pady=30, padx=30, fill="both", expand=True)

        fields = {
            "product_id": tk.StringVar(value=product.get("product_id", "")),
            "name": tk.StringVar(value=product.get("name", "")),
            "price": tk.StringVar(value=product.get("price", "0")),
            "stock": tk.StringVar(value=product.get("stock", "0")),
            "category": tk.StringVar(value=product.get("category", "موبایل")),
            "image": tk.StringVar(value=product.get("image", ""))
        }
        labels = {
            "product_id": ":شناسه کالا",
            "name": ":نام کالا",
            "price": ":قیمت",
            "stock": ":موجودی",
            "category": ":دسته",
            "image": ":مسیر تصویر"
        }

        for key, label_text in labels.items():
            row = tk.Frame(form_frame, bg="white")
            row.pack(fill="x", pady=8)
            label = tk.Label(
                row,
                text=f"{label_text}",
                font=("Arial", 12, "bold"),
                bg="white",
                width=14,
                anchor="e"
            )
            label.pack(side="right", padx=(0, 10))

            if key == "category":
                cb = ttk.Combobox(row, textvariable=fields[key], values=("موبایل", "لپ‌تاپ", "هدفون", "ساعت", "دیجیتال"), state="readonly", font=("Arial", 11))
                cb.pack(side="right", ipady=2, ipadx=20, padx=(0, 15))
            elif key == "image":
                entry = tk.Entry(row, textvariable=fields[key], font=("Arial", 10), bg="white", fg="black", bd=1, relief="solid", width=20)
                entry.pack(side="right", ipady=2, ipadx=20, padx=(0, 15))
                def browse():
                    path = filedialog.askopenfilename(title="انتخاب تصویر محصول", filetypes=[("Image files", "*.png *.jpg *.jpeg")])
                    if path:
                        fields["image"].set(path)
                tk.Button(row, text="🔍", command=browse, bg="lightgray", width=3).pack(side="right")
            else:
                entry = tk.Entry(row, textvariable=fields[key], font=("Arial", 10), bg="white", fg="black", bd=1, relief="solid", width=20)
                entry.pack(side="right", ipady=2, ipadx=20, padx=(0, 15))

        # --- نمایش خطا ---
        error_label = tk.Label(
            edit_win,
            text="",
            font=("Arial", 10, "bold"),
            fg="red",
            bg="white",
            wraplength=900,
            justify="right"
        )
        error_label.pack(pady=5)

        def save():
            data = {k: v.get().strip() for k, v in fields.items()}
            if not all(data.values()):
                error_label.config(text=" .لطفاً همه فیلدها را پر کنید")
                return
            try:
                int(data["price"])
                int(data["stock"])
            except:
                error_label.config(text=" .قیمت و موجودی باید عدد باشند")
                return
            error_label.config(text="")  # پاک کردن خطا
            product.update(data)
            product["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
            save_products_to_csv()
            refresh_table()
            edit_win.destroy()

        tk.Button(
            edit_win,
            text=" ذخیره تغییرات",
            bg=THEME_COLOR,
            fg="white",
            font=("Arial", 14, "bold"),
            width=20,
            height=2,
            command=save
        ).pack(pady=40)

    # --- فریم دکمه‌های حذف و ویرایش ---
    btn_frame = tk.Frame(main_frame, bg="white", height=50)
    btn_frame.pack(fill="x", pady=(10, 0))
    btn_frame.pack_propagate(False)

    # --- نمایش خطا  ---
    error_label = tk.Label(
        btn_frame,
        text="",
        font=("Arial", 11, "bold"),
        fg="red",
        bg="white"
    )
    error_label.pack(side="left", padx=(385,10))
    tk.Button(btn_frame, text="ویرایش", bg="#FF9800", fg="white", font=("Arial", 11, "bold"), command=edit_product).pack(side="right", padx=5)
    tk.Button(btn_frame, text=" حذف", bg="#F44336", fg="white", font=("Arial", 11, "bold"), command=delete_product).pack(side="right", padx=5)
    load_products_from_csv()
#------نمایش سفارشات------
def show_orders():
    win = tk.Toplevel()
    win.title(" لیست سفارشات")
    center_window(win, 1000, 600)
    win.configure(bg="white")
    win.resizable(False, False)

    # --- متغیرها ---
    orders = []
    original_orders = []

    # --- تابع بارگذاری سفارشات از فایل ---
    def load_orders():
        nonlocal orders, original_orders
        try:
            with open('orders.csv', 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                orders = []
                for row in reader:
                    cleaned_row = {key.strip(): value for key, value in row.items()}
                    if '\ufeffusername' in cleaned_row:
                        cleaned_row['username'] = cleaned_row.pop('\ufeffusername')

                    order = {
                        "username": get_user_full_name(cleaned_row.get("username", "ناشناس")),
                        "product_id": cleaned_row.get("product_id", "ناشناس"),
                        "quantity": cleaned_row.get("quantity", "0"),
                        "total_price": cleaned_row.get("total_price", "0"),
                        "date": cleaned_row.get("date", "تاریخ نامشخص")
                    }
                    orders.append(order)
                original_orders = orders.copy()
                print(f" {len(orders)} سفارش با موفقیت بارگذاری شد.")
        except FileNotFoundError:
            messagebox.showerror("خطا", "فایل 'orders.csv' یافت نشد!")
            win.destroy()
            return
        except Exception as e:
            messagebox.showerror("خطا", f"خطا در خواندن فایل:\n{str(e)}")
            win.destroy()
            return
        refresh_table()

    # --- تابع فیلتر جستجو ---
    def apply_search():
        query = search_var.get().strip().lower()
        filtered = original_orders
        if query and query != "":
            filtered = [
                o for o in filtered
                if query in o["username"].lower() or
                   query in o["product_id"].lower() or
                   query in o["total_price"]
            ]
        orders[:] = filtered
        refresh_table()

    # --- تابع بازسازی جدول ---
    def refresh_table():
        for row in tree.get_children():
            tree.delete(row)
        for order in orders:
            product_name = get_product_name_by_id(order["product_id"])  # 👈 نام واقعی کالا
            tree.insert("", "end", values=(
                order["username"],
                product_name,
                order["quantity"],
                f"{int(order['total_price']):,}",
                order["date"]
            ))

    # --- نوار بالایی ---
    nav_bar = tk.Frame(win, bg=THEME_COLOR, height=80)
    nav_bar.pack(side="top", fill="x")

    #--- لوگو ---
    try:
        nav_logo = PhotoImage(file="shopera_nav_logo.png")
        logo_label = tk.Label(nav_bar, image=nav_logo, bg=THEME_COLOR)
        logo_label.image = nav_logo
    except Exception as e:
        print(f"⚠️ لوگو بارگذاری نشد: {e}")
        logo_label = tk.Label(nav_bar, text="Shopera", font=("Arial", 16, "bold"), fg="white", bg=THEME_COLOR)
    logo_label.pack(side="right", padx=10)

    # --- کادر جستجو ---
    search_frame = tk.Frame(nav_bar, bg="white", height=35)
    search_frame.pack(side="right", padx=10, pady=20)

    search_var = tk.StringVar()
    search_entry = tk.Entry(
        search_frame,
        textvariable=search_var,
        font=("Arial", 12),
        fg="gray",
        bg="white",
        relief="flat",
        bd=0,
        highlightthickness=0,
        justify="right",
        width=25
    )
    search_entry.insert(0, "...جستجو")
    search_entry.pack(side="left", padx=(5, 0))

    def on_focus_in(event):
        if search_entry.get() == "...جستجو":
            search_entry.delete(0, tk.END)
            search_entry.config(fg="black")

    def on_focus_out(event):
        if search_entry.get() == "":
            search_entry.insert(0, "...جستجو")
            search_entry.config(fg="gray")

    search_entry.bind("<FocusIn>", on_focus_in)
    search_entry.bind("<FocusOut>", on_focus_out)

    try:
        search_icon = PhotoImage(file="search_icon.png")
        search_btn = tk.Button(search_frame, image=search_icon, bg="white", bd=0, command=apply_search)
        search_btn.image = search_icon
    except:
        search_btn = tk.Button(search_frame, text="🔍", font=("Arial", 12), bg="white", bd=0, command=apply_search)
    search_btn.pack(side="right", padx=(0, 5))

    # --- دکمه بازگشت ---
    buttons_frame = tk.Frame(nav_bar, bg=THEME_COLOR)
    buttons_frame.pack(side="left", padx=10)

    try:
        back_img = PhotoImage(file="backright.png").subsample(2, 2)
        back_btn = tk.Button(
            buttons_frame,
            image=back_img,
            bg=THEME_COLOR,
            activebackground=THEME_COLOR,
            bd=0,
            highlightthickness=0,
            relief="flat",
            command=win.destroy
        )
        back_btn.image = back_img
    except Exception as e:
        print(f"⚠️ آیکون بازگشت بارگذاری نشد: {e}")
        back_btn = tk.Button(
            buttons_frame,
            text="بازگشت",
            font=("Arial", 11),
            bg=THEME_COLOR,
            fg="white",
            activebackground=THEME_COLOR,
            activeforeground="white",
            bd=0,
            highlightthickness=0,
            relief="flat",
            command=win.destroy
        )
    back_btn.pack(side="left", padx=5)

    # --- عنوان صفحه ---
    tk.Label(
        win,
        text=" لیست سفارشات ثبت‌شده",
        font=("Arial", 18, "bold"),
        fg=THEME_COLOR,
        bg="white"
    ).pack(pady=(10, 5))

    # --- فریم مرکزی ---
    main_frame = tk.Frame(win, bg="white")
    main_frame.pack(fill="both", expand=True, padx=20, pady=10)

    # --- فریم جدول و اسکرول ---
    tree_frame = tk.Frame(main_frame)
    tree_frame.pack(fill="both", expand=True)

    # --- اسکرول عمودی ---
    scrollbar = ttk.Scrollbar(tree_frame)
    scrollbar.pack(side="right", fill="y")

    # --- جدول ---
    columns = ("username", "product_id", "quantity", "total_price", "date")
    tree = ttk.Treeview(
        tree_frame,
        columns=columns,
        show="headings",
        height=10,
        yscrollcommand=scrollbar.set
    )
    tree.pack(fill="both", expand=True)
    scrollbar.config(command=tree.yview)

    # --- سرستون‌ها ---
    tree.heading("username", text="نام کاربر")
    tree.heading("product_id", text="نام کالا")
    tree.heading("quantity", text="تعداد")
    tree.heading("total_price", text="جمع کل")
    tree.heading("date", text="تاریخ و زمان")

    # --- تنظیم عرض ستون‌ها ---
    tree.column("username", width=180, anchor="center")
    tree.column("product_id", width=140, anchor="center")
    tree.column("quantity", width=100, anchor="center")
    tree.column("total_price", width=160, anchor="center")
    tree.column("date", width=170, anchor="center")

    # --- استایل ---
    style = ttk.Style()
    style.configure("Treeview", rowheight=35, font=("Arial", 10))
    style.configure("Treeview.Heading", font=("Arial", 11, "bold"), foreground=THEME_COLOR)

    # --- هاور افکت ---
    tree.tag_configure("hover", background="#f0f8ff")
    def on_hover(event):
        item = tree.identify_row(event.y)
        for i in tree.get_children():
            tree.item(i, tags=())
        if item:
            tree.item(item, tags=("hover",))
    tree.bind("<Motion>", on_hover)

    # --- فریم دکمه‌ها ---
    btn_frame = tk.Frame(main_frame, bg="white", height=50)
    btn_frame.pack(fill="x", pady=(10, 0))
    btn_frame.pack_propagate(False)

    # دکمه پرینت
    print_btn = tk.Button(
        btn_frame,
        text="پرینت لیست",
        bg=THEME_COLOR,
        fg="white",
        font=("Arial", 11, "bold")
    )
    print_btn.pack(side="right", padx=5)

    # لیبل پیام
    print_status_label = tk.Label(
        btn_frame,
        text="",
        font=("Arial", 11),
        fg="green",
        bg="white"
    )
    print_status_label.pack(side="right", padx=10)

    # --- تابع پرینت با نمایش پیام در صفحه ---
    def on_print_click():
        print_status_label.config(text="...در حال ارسال به چاپگر")
        # بعد از 2 ثانیه پیام پاک بشه (اختیاری)
        win.after(2000, lambda: print_status_label.config(text=""))

    # اتصال تابع به دکمه
    print_btn.config(command=on_print_click)

    # --- بارگذاری اولیه ---
    load_orders()
# --- گزارش فروش ---
def show_sales_report():
    win = tk.Toplevel()
    win.title(" گزارش فروش")
    center_window(win, 1000, 600)
    win.configure(bg="white")
    win.resizable(False, False)

    # --- متغیرها ---
    sales_data = []

    # --- تابع بارگذاری و محاسبه گزارش فروش ---
    def load_sales_report():
        nonlocal sales_data
        from collections import defaultdict
        sales = defaultdict(lambda: {"quantity": 0, "total": 0})

        try:
            with open('orders.csv', 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    cleaned_row = {k.strip(): v for k, v in row.items()}
                    if '\ufeffusername' in cleaned_row:
                        cleaned_row['username'] = cleaned_row.pop('\ufeffusername')

                    product_id = cleaned_row.get("product_id", "ناشناس")
                    try:
                        qty = int(cleaned_row.get("quantity", 0))
                        total_price = int(cleaned_row.get("total_price", 0))
                    except:
                        continue

                    sales[product_id]["quantity"] += qty
                    sales[product_id]["total"] += total_price

            # تبدیل به لیست قابل نمایش
            sales_data = []
            for pid, data in sales.items():
                sales_data.append({
                    "product_id": pid,
                    "quantity": str(data["quantity"]),
                    "total_price": str(data["total"])
                })
            print(f" گزارش فروش برای {len(sales_data)} محصول محاسبه شد.")
        except FileNotFoundError:
            messagebox.showerror("خطا", "فایل 'orders.csv' یافت نشد!")
            win.destroy()
            return
        except Exception as e:
            messagebox.showerror("خطا", f"خطا در خواندن فایل:\n{str(e)}")
            win.destroy()
            return
        refresh_table()

    # --- تابع بازسازی جدول ---
    def refresh_table():
        for row in tree.get_children():
            tree.delete(row)
        for item in sales_data:
            product_name = get_product_name_by_id(item["product_id"])  # 👈 نام کالا
            tree.insert("", "end", values=(
                product_name,
                item["quantity"],
                f"{int(item['total_price']):,}"
            ))

    # --- نوار بالایی ---
    nav_bar = tk.Frame(win, bg=THEME_COLOR, height=80)
    nav_bar.pack(side="top", fill="x")

    # --- لوگو ---
    try:
        nav_logo = PhotoImage(file="shopera_nav_logo.png")
        logo_label = tk.Label(nav_bar, image=nav_logo, bg=THEME_COLOR)
        logo_label.image = nav_logo
    except Exception as e:
        print(f"⚠️ لوگو بارگذاری نشد: {e}")
        logo_label = tk.Label(nav_bar, text="Shopera", font=("Arial", 16, "bold"), fg="white", bg=THEME_COLOR)
    logo_label.pack(side="right", padx=10)

    # --- کادر جستجو ---
    search_frame = tk.Frame(nav_bar, bg="white", height=35)
    search_frame.pack(side="right", padx=10, pady=20)

    search_var = tk.StringVar()
    search_entry = tk.Entry(
        search_frame,
        textvariable=search_var,
        font=("Arial", 12),
        fg="gray",
        bg="white",
        relief="flat",
        bd=0,
        highlightthickness=0,
        justify="right",
        width=25
    )
    search_entry.insert(0, "...جستجو")
    search_entry.pack(side="left", padx=(5, 0))

    def on_focus_in(event):
        if search_entry.get() == "...جستجو":
            search_entry.delete(0, tk.END)
            search_entry.config(fg="black")

    def on_focus_out(event):
        if search_entry.get() == "":
            search_entry.insert(0, "جستجو...")
            search_entry.config(fg="gray")

    search_entry.bind("<FocusIn>", on_focus_in)
    search_entry.bind("<FocusOut>", on_focus_out)

    try:
        search_icon = PhotoImage(file="search_icon.png")
        search_btn = tk.Button(search_frame, image=search_icon, bg="white", bd=0, command=lambda: apply_search(search_var.get()))
        search_btn.image = search_icon
    except:
        search_btn = tk.Button(search_frame, text="🔍", font=("Arial", 12), bg="white", bd=0, command=lambda: apply_search(search_var.get()))
    search_btn.pack(side="right", padx=(0, 5))

    # --- تابع فیلتر جستجو ---
    def apply_search(query):
        query = query.strip().lower()
        filtered = []
        for item in sales_data:
            if (query in item["product_id"].lower() or
                query in item["quantity"] or
                query in item["total_price"]):
                filtered.append(item)
        # نمایش نتایج فیلتر شده
        for row in tree.get_children():
            tree.delete(row)
        for item in filtered:
            tree.insert("", "end", values=(
                item["product_id"],
                item["quantity"],
                f"{int(item['total_price']):,}" if item['total_price'].isdigit() else item['total_price']
            ))

    # --- دکمه بازگشت ---
    buttons_frame = tk.Frame(nav_bar, bg=THEME_COLOR)
    buttons_frame.pack(side="left", padx=10)

    try:
        back_img = PhotoImage(file="backright.png").subsample(2, 2)
        back_btn = tk.Button(
            buttons_frame,
            image=back_img,
            bg=THEME_COLOR,
            activebackground=THEME_COLOR,
            bd=0,
            highlightthickness=0,
            relief="flat",
            command=win.destroy
        )
        back_btn.image = back_img
    except Exception as e:
        print(f"⚠️ آیکون بازگشت بارگذاری نشد: {e}")
        back_btn = tk.Button(
            buttons_frame,
            text="بازگشت",
            font=("Arial", 11),
            bg=THEME_COLOR,
            fg="white",
            activebackground=THEME_COLOR,
            activeforeground="white",
            bd=0,
            highlightthickness=0,
            relief="flat",
            command=win.destroy
        )
    back_btn.pack(side="left", padx=5)

    # --- عنوان صفحه ---
    tk.Label(
        win,
        text="گزارش فروش بر اساس کالا",
        font=("Arial", 18, "bold"),
        fg=THEME_COLOR,
        bg="white"
    ).pack(pady=(10, 5))

    # --- فریم مرکزی ---
    main_frame = tk.Frame(win, bg="white")
    main_frame.pack(fill="both", expand=True, padx=20, pady=10)

    # --- فریم جدول و اسکرول ---
    tree_frame = tk.Frame(main_frame)
    tree_frame.pack(fill="both", expand=True)

    # --- اسکرول عمودی ---
    scrollbar = ttk.Scrollbar(tree_frame)
    scrollbar.pack(side="right", fill="y")

    # --- جدول ---
    columns = ("product_id", "quantity", "total_price")
    tree = ttk.Treeview(
        tree_frame,
        columns=columns,
        show="headings",
        height=8,
        yscrollcommand=scrollbar.set
    )
    tree.pack(fill="both", expand=True)
    scrollbar.config(command=tree.yview)

    # --- سرستون‌ها ---
    tree.heading("product_id", text="نام کالا")
    tree.heading("quantity", text="مجموع تعداد فروش")
    tree.heading("total_price", text="جمع فروش")

    # --- تنظیم عرض ستون‌ها ---
    tree.column("product_id", width=200, anchor="center")
    tree.column("quantity", width=160, anchor="center")
    tree.column("total_price", width=200, anchor="center")

    # --- استایل ---
    style = ttk.Style()
    style.configure("Treeview", rowheight=35, font=("Arial", 11))
    style.configure("Treeview.Heading", font=("Arial", 12, "bold"), foreground=THEME_COLOR)

    # --- هاور افکت ---
    tree.tag_configure("hover", background="#f0f8ff")
    def on_hover(event):
        item = tree.identify_row(event.y)
        for i in tree.get_children():
            tree.item(i, tags=())
        if item:
            tree.item(item, tags=("hover",))
    tree.bind("<Motion>", on_hover)

    # --- فریم دکمه‌ها ---
    btn_frame = tk.Frame(main_frame, bg="white", height=50)
    btn_frame.pack(fill="x", pady=(10, 0))
    btn_frame.pack_propagate(False)

    # --- دکمه پرینت ---
    print_btn = tk.Button(
        btn_frame,
        text="پرینت گزارش",
        bg=THEME_COLOR,
        fg="white",
        font=("Arial", 11, "bold")
    )
    print_btn.pack(side="right", padx=5)

    # --- لیبل پیام ---
    print_status_label = tk.Label(
        btn_frame,
        text="",
        font=("Arial", 11),
        fg="green",
        bg="white"
    )
    print_status_label.pack(side="right", padx=10)

    # --- تابع پرینت با نمایش پیام در صفحه ---
    def on_print_click():
        print_status_label.config(text="...در حال ارسال گزارش به چاپگر")
        # بعد از 2 ثانیه پیام پاک بشه
        win.after(2000, lambda: print_status_label.config(text=""))

    # اتصال تابع به دکمه
    print_btn.config(command=on_print_click)

    # --- بارگذاری اولیه ---
    load_sales_report()

# --- لوگو ابتدایی ---
def show_logo():
    root = tk.Tk()
    root.title("Shopera Logo")
    root.geometry("1000x600+200+100")
    root.resizable(False, False)
    center_window(root, 1000, 600)

    try:
        logo_image = PhotoImage(file="logo.png")
        label = tk.Label(root, image=logo_image)
        label.image = logo_image
    except:
        label = tk.Label(root, text="Shopera", font=("Arial", 40, "bold"), fg=THEME_COLOR)

    label.pack(expand=True)
    root.after(5000, root.destroy)
    root.mainloop()
# --- نمایش صفحه محصول ---
from tkinter import Toplevel, Label, PhotoImage

def open_product_page(name, price, image_filename):
    new_window = Toplevel()
    new_window.title(name)
    new_window.geometry("560x600")  # اندازه بزرگتر برای نمایش بهتر تصویر

    # مسیر کامل تصویر
    full_image_path = os.path.join("product_pics", image_filename)

    try:
        img = PhotoImage(file=full_image_path)
        img_label = Label(new_window, image=img)
        img_label.image = img  # جلوگیری از پاک شدن عکس
        img_label.pack(pady=10)
    except Exception as e:
        print(f"❌ تصویر یافت نشد: {full_image_path}")
        print(f"جزئیات خطا: {e}")
        img_label = Label(new_window, text="تصویر موجود نیست", font=("Arial", 12))
        img_label.pack(pady=10)

    Label(new_window, text=name, font=("Arial", 16, "bold"), fg=THEME_COLOR).pack(pady=5)
    Label(new_window, text=f"{price} تومان", font=("Arial", 12), fg="red").pack(pady=5)

# --- ساخت نوار تخفیف ---
def create_discount_bar(parent):
    discount_frame = tk.Frame(parent, bg=DISCOUNT_BAR_COLOR, width=900, height=150)
    discount_frame.pack(pady=(0, 10))
    discount_frame.pack_propagate(False)
    # آیکن درصد
    try:
        percent_img = PhotoImage(file="percent.png")
        percent_label = tk.Label(discount_frame, image=percent_img, bg=DISCOUNT_BAR_COLOR)
        percent_label.image = percent_img
    except:
        percent_label = tk.Label(discount_frame, text="٪", font=("Arial", 20, "bold"), bg=DISCOUNT_BAR_COLOR,
                                 fg="white")
    percent_label.pack(side="right", padx=(7, 2), pady=10)

    # لیست محصولات از دسته‌بندی‌های مختلف
    products_frame = tk.Frame(discount_frame, bg=DISCOUNT_BAR_COLOR)
    products_frame.pack(fill="both", expand=True, padx=(0, 0))

    # ۵ محصول از ۵ دسته‌بندی مختلف
    categories = [
        ("موبایل", "موبایل سامسونگ گلکسی", "30,000,000 ", "موبایل_1.png"),
        ("لپ‌تاپ", "لپ‌تاپ اپل مک‌بوک", "70,000,000 ", "لپ‌تاپ_1.png"),
        ("دیجیتال", "تبلت سامسونگ تب ", "25,000,000 ", "دیجیتال_1.png"),
        ("هدفون", "هدفون بلوتوثی سونی", "12,000,000 ", "هدفون_1.png"),
        ("ساعت", "  ساعت اپل واچ   ", "15,000,000 ", "ساعت_4.png")
    ]

    images_list = []  # لیست برای نگه‌داری تصاویر

    for category, name, price, image_file in categories:
        item_frame = tk.Frame(products_frame, bg="white")
        item_frame.pack(side="right", padx=10, pady=10)

        # مسیر کامل تصویر
        image_path = f"image/{image_file}"

        try:
            img = PhotoImage(file=image_path).subsample(2, 2)
            images_list.append(img)  # ذخیره تصویر برای جلوگیری از پاک شدن

            # ایجاد دکمه با تصویر
            img_button = tk.Button(item_frame, image=img, bg="white", bd=0,
                                   command=lambda n=name, p=price, i=image_path, c=category: show_product_details({
                                       "name": n,
                                       "price": p,
                                       "image": i,
                                       "features": [
                                           f"دسته‌بندی: {c} •",
                                           "ویژگی‌های نمونه محصول •",
                                           "کیفیت عالی و ضمانت •"
                                       ]
                                   }))
            img_button.image = img
            img_button.pack(padx=5, pady=(5, 2))
        except Exception as e:
            print(f"خطا در بارگذاری تصویر {image_path}: {e}")
            # اگر تصویر وجود نداشت، از دکمه متنی استفاده کن
            tk.Button(item_frame, text=name,
                      command=lambda n=name, p=price, c=category: show_product_details({
                          "name": n,
                          "price": p,
                          "image": "default.png",
                          "features": [
                              f"دسته‌بندی: {c} •",
                              "ویژگی‌های نمونه محصول •",
                              "کیفیت عالی و ضمانت •"
                          ]
                      }),
                      bg="white", fg=THEME_COLOR, font=("Arial", 10)).pack(padx=5, pady=(5, 2))

        # نام محصول
        tk.Label(item_frame, text=name, font=("Arial", 11, "bold"), bg="white", fg=THEME_COLOR,padx=5).pack()
        # قیمت
        tk.Label(item_frame, text=f" {price}تومان ", font=("Arial", 10), bg="white", fg="red").pack()
# --- ثبت نام ---

def open_register(parent, login_button_to_hide, nav_bar):
    register_win = tk.Toplevel(parent)
    register_win.title("ثبت‌نام")
    register_win.geometry("1000x600+200+100")
    register_win.resizable(False, False)
    center_window(register_win, 1000, 600)
    try:
        bg_image = PhotoImage(file="back.png")
        tk.Label(register_win, image=bg_image).place(x=0, y=0, relwidth=1, relheight=1)
        register_win.bg_image = bg_image
    except:
        register_win.configure(bg=BG_COLOR)

    tk.Label(register_win, text="ثبت‌نام", font=("Arial", 24), fg=THEME_COLOR, bg="white").place(x=250, y=280)

    firstname_entry = create_entry_with_placeholder(register_win, "نام")
    lastname_entry = create_entry_with_placeholder(register_win, "نام خانوادگی")
    username_entry = create_entry_with_placeholder(register_win, "نام کاربری")
    password_entry = create_entry_with_placeholder(register_win, "رمز ورود", show_char="*")
    firstname_entry.place(x=560, y=220, width=260, height=35)
    lastname_entry.place(x=560, y=260, width=260, height=35)
    username_entry.place(x=560, y=300, width=260, height=35)
    password_entry.place(x=560, y=340, width=260, height=35)

    tk.Label(register_win, text=":جنسیت", font=("Arial", 12), bg="white", fg=THEME_COLOR).place(x=760, y=380)
    gender_var = tk.StringVar(value="زن")
    tk.Radiobutton(register_win, text="زن", variable=gender_var, value="زن", font=("Arial", 11), bg="white",
                   fg=THEME_COLOR).place(x=695, y=380)
    tk.Radiobutton(register_win, text="مرد", variable=gender_var, value="مرد", font=("Arial", 11), bg="white",
                   fg=THEME_COLOR).place(x=640, y=380)

    error_label = tk.Label(register_win, text="", fg="red", bg="white", font=("Arial", 10))
    error_label.place(x=565, y=400)
# --- ثبت نام ---
    def handle_register():
        global default_mode
        default_mode = False

        firstname = firstname_entry.get()
        lastname = lastname_entry.get()
        username = username_entry.get()
        password = password_entry.get()
        gender = gender_var.get()

        # بررسی پر بودن فیلدها
        if firstname in ["", "نام"] or lastname in ["", "نام خانوادگی"] or username in ["",
                                                                                        "نام کاربری"] or password in [
            "", "رمز ورود"]:
            error_label.config(text="همه‌ی فیلدها باید پر شوند")
            return

        # ---بررسی امنیت رمز عبور ---
        if len(password) < 6:
            error_label.config(text="رمز عبور باید حداقل 6 کاراکتر باشد")
            return

        if not re.search(r"[a-zA-Z]", password):
            error_label.config(text="رمز عبور باید شامل حروف انگلیسی باشد")
            return

        if not re.search(r"[0-9]", password):
            error_label.config(text="رمز عبور باید شامل عدد باشد")
            return

        # بررسی تکراری بودن نام کاربری
        if username in users_db:
            error_label.config(text="نام کاربری قبلا استفاده شده است")
            return

        # اضافه کردن کاربر
        users_db[username] = {
            'password': password,
            'balance': 0,
            'role': 'user',
            'firstname': firstname,
            'lastname': lastname,
            'gender': gender
        }

        save_users(users_db)

        # ورود خودکار بعد از ثبت‌نام
        global current_user
        current_user = {
            "username": username,
            "firstname": firstname,
            "lastname": lastname,
            "role": "user",
            "balance": 0,
            "gender": gender
        }

        # بستن پنجره‌ها
        register_win.destroy()
        parent.destroy()

        for w in parent.master.winfo_children():
            if isinstance(w, tk.Toplevel):
                w.destroy()

        # نمایش دکمه خروج
        login_button_to_hide.pack_forget()
        logout_button = tk.Button(
            nav_bar,
            text="خروج از حساب",
            font=("Arial", 11),
            bg="white",
            fg=THEME_COLOR,
            command=lambda: logout(nav_bar, login_button_to_hide)
        )
        logout_button.pack(side="left", padx=(10, 5), pady=20)

        messagebox.showinfo("موفقیت", "ثبت‌نام با موفقیت انجام شد!")

        # بستن پنجره‌ها
        register_win.destroy()
        parent.destroy()

        # بستن پنجره‌های اضافی
        for w in parent.master.winfo_children():
            if isinstance(w, tk.Toplevel):
                w.destroy()

    tk.Button(register_win, text="ثبت‌نام", font=("Arial", 12, "bold"), fg="white", bg=THEME_COLOR,
              command=handle_register).place(x=630, y=445, width=100, height=38)

# --- ورود ---
def open_login(parent, login_button_to_hide, nav_bar):
    #  تعریف اولیه logout_button در ابتدای تابع
    logout_button = None

    login_win = tk.Toplevel(parent)
    login_win.title("ورود")
    login_win.geometry("1000x600+200+100")
    login_win.resizable(False, False)
    center_window(login_win, 1000, 600)

    try:
        bg_image = PhotoImage(file="login_bg.png")
        tk.Label(login_win, image=bg_image).place(x=0, y=0, relwidth=1, relheight=1)
        login_win.bg_image = bg_image
    except:
        login_win.configure(bg=BG_COLOR)

    tk.Label(login_win, text="ورود", font=("Arial", 24), fg=THEME_COLOR, bg="white").place(x=250, y=179)

    tk.Button(login_win, text="ثبت‌نام", font=("Arial", 11), fg=THEME_COLOR, bg=BG_COLOR,
              command=lambda: open_register(login_win, login_button_to_hide, nav_bar)).place(x=675, y=480)

    username_entry = create_entry_with_placeholder(login_win, "نام کاربری")
    password_entry = create_entry_with_placeholder(login_win, "رمز ورود", show_char="*")
    username_entry.place(x=560, y=260, width=260, height=35)
    password_entry.place(x=560, y=340, width=260, height=35)
    error_label = tk.Label(login_win, text="", fg="red", bg="white", font=("Arial", 10))
    error_label.place(x=563, y=387)

    # --- ورود ---
    def handle_login():
        nonlocal logout_button  # ✅ حالا مجازه، چون logout_button در تابع بیرونی تعریف شده
        username = username_entry.get().strip()
        password = password_entry.get().strip()

        global current_user

        # حالت تست
        if default_mode and username == "1234" and password == "1234":
            current_user = {
                "username": username,
                "password": "1234",
                "balance": 1000000,
                "role": "admin",
                "firstname": "کاربر",
                "lastname": "تستی",
                "gender": "ناشناس"
            }
            login_win.destroy()
            login_button_to_hide.pack_forget()

            logout_button = tk.Button(
                nav_bar,
                text="خروج از حساب",
                font=("Arial", 11),
                bg="white",
                fg=THEME_COLOR,
                command=lambda: logout(nav_bar, login_button_to_hide)
            )
            logout_button.pack(side="left", padx=(10, 5), pady=20)

            show_admin_panel()
            return

        # بررسی کاربر عادی
        if username in users_db and users_db[username]['password'] == password:
            user_data = users_db[username]

            current_user = {
                "username": username,
                "password": user_data["password"],
                "balance": user_data["balance"],
                "role": user_data["role"],
                "firstname": user_data["firstname"],
                "lastname": user_data["lastname"],
                "gender": user_data.get("gender", "ناشناس")
            }

            login_win.destroy()
            login_button_to_hide.pack_forget()

            logout_button = tk.Button(
                nav_bar,
                text="خروج از حساب",
                font=("Arial", 11),
                bg="white",
                fg=THEME_COLOR,
                command=lambda: logout(nav_bar, login_button_to_hide)
            )
            logout_button.pack(side="left", padx=(10, 5), pady=20)

            if user_data['role'] == 'admin':
                show_admin_panel()
        else:
            error_label.config(text="نام کاربری یا رمز عبور اشتباه است")

    tk.Button(login_win, text="ورود", font=("Arial", 12, "bold"), fg="white", bg=THEME_COLOR,
              command=handle_login).place(x=648, y=415, width=100, height=38)
# --- خروج از حساب ---
def logout(nav_bar, login_button_to_show):
    global current_user
    current_user = None
    for widget in nav_bar.winfo_children():
        if isinstance(widget, tk.Button) and widget.cget("text") == "خروج از حساب":
            widget.destroy()
    login_button_to_show.pack(side="left", padx=(10, 5), pady=20)

from tkinter import messagebox
# --- حساب کاربری ---
def try_show_cart():
    if current_user is None:
        messagebox.showwarning("دسترسی محدود", "لطفاً ابتدا وارد حساب کاربری خود شوید.")
    else:
        show_cart_window()
# --- صفحه اصلی ---
def main_app():
    root = tk.Tk()
    center_window(root, 1000, 600)
    root.title("Shopera Main")
    root.geometry("1000x600")
    root.configure(bg=BG_COLOR)
    root.resizable(False, False)
    # نوار بالایی
    nav_bar = tk.Frame(root, bg=THEME_COLOR, height=80)
    nav_bar.pack(side="top", fill="x")
    try:
        nav_logo = PhotoImage(file="shopera_nav_logo.png")
        logo_label = tk.Label(nav_bar, image=nav_logo, bg=THEME_COLOR)
        logo_label.image = nav_logo
    except:
        logo_label = tk.Label(nav_bar, text="Shopera", font=("Arial", 16, "bold"), fg="white", bg=THEME_COLOR)
    logo_label.pack(side="right", padx=10)
    # --- فریم نوار بالا ---
    buttons_frame = tk.Frame(nav_bar, bg=THEME_COLOR)
    buttons_frame.pack(side="left", padx=10)
    # جستجو
    search_frame = tk.Frame(nav_bar, bg="white", height=35)
    search_frame.pack(side="right", padx=10, pady=20)

    # ایجاد نوار جستجو با placeholder بهبود یافته
    search_entry = tk.Entry(
        search_frame,
        font=("Arial", 12),
        fg="black",
        bg="white",
        relief="flat",  # حذف حاشیه مستطیل
        bd=0,  # حذف کامل حاشیه
        highlightthickness=0,  # غیرفعال کردن خط دور
        justify="right"
    )
    search_entry.bind("<Button-1>", lambda e: search_entry.delete(0, tk.END))
    # اضافه کردن متن پیش‌فرض
    search_entry.insert(0, "...جستجو")

    # مدیریت placeholder (متن پیش‌فرض)
    def on_focus_in(event):
        if search_entry.get() == "...جستجو":
            search_entry.delete(0, tk.END)
            search_entry.config(fg="black")

    def on_focus_out(event):
        if search_entry.get() == "":
            search_entry.insert(0, "...جستجو")
            search_entry.config(fg="gray")

    search_entry.bind("<FocusIn>", on_focus_in)
    search_entry.bind("<FocusOut>", on_focus_out)
    search_entry.pack(side="left", padx=(5, 0))

    # تابع برای انجام جستجو
    def perform_search():
        try:
            query = search_entry.get().strip()

            if query == "...جستجو" or not query:
                return

            # دیکشنری جستجو
            category_mapping = {
                "موبایل": "موبایل",
                "موبايل": "موبایل",
                "گوشی": "موبایل",
                "گوشي": "موبایل",
                "mobile": "موبایل",
                "لپ تاپ": "لپ‌تاپ",
                "لپتاپ": "لپ‌تاپ",
                "لپ": "لپ‌تاپ",
                "هدفون": "هدفون",
                "هدست": "هدفون",
                "ساعت": "ساعت",
                "دیجیتال": "دیجیتال"
            }

            # نرمالایز کردن query
            normalized_query = query.lower().replace(" ", "").replace("‌", "").replace("ي", "ی")

            # جستجو
            matched_category = None
            for key, value in category_mapping.items():
                normalized_key = key.lower().replace(" ", "").replace("‌", "").replace("ي", "ی")
                if normalized_query == normalized_key:
                    matched_category = value
                    break

            # بازگرداندن متن پیشفرض بدون توجه به نتیجه جستجو
            search_entry.delete(0, tk.END)
            search_entry.insert(0, "...جستجو")
            search_entry.config(fg="black")

            if matched_category:
                show_category_products(matched_category)
            else:
                messagebox.showinfo(
                    "نتیجه جستجو",
                    f"عبارت '{query}' یافت نشد\n\n"
                    "کلیدواژه‌های معتبر:\n"
                    "- موبایل\n- لپ‌تاپ\n- هدفون\n- ساعت\n- دیجیتال"
                )
            search_entry.delete(0, tk.END)
            search_entry.insert(0, "...جستجو")
        except Exception as e:
            messagebox.showerror("خطا", f"خطا در جستجو: {str(e)}")
            # در صورت خطا هم متن پیشفرض بازگردانده شود
            search_entry.delete(0, tk.END)
            search_entry.insert(0, "...جستجو")
            search_entry.config(fg="gray")

    # ایجاد دکمه ذره‌بین با عملکرد جستجو
    try:
        search_icon = PhotoImage(file="search_icon.png")
        search_btn = tk.Button(search_frame, image=search_icon, bg="white", bd=0, command=perform_search)
        search_btn.image = search_icon
    except:
        search_btn = tk.Button(search_frame, text="🔍", font=("Arial", 12), bg="white", bd=0, command=perform_search)
    search_btn.pack(side="right", padx=(0, 5))
    logout_button = None
    login_button = tk.Button(nav_bar, text="ورود / ثبت‌نام", font=("Arial", 11, "bold"), bg="white", fg=THEME_COLOR,
                             command=lambda: open_login(root, login_button, nav_bar))
    login_button.pack(side="left", padx=(5, 5), pady=20)
    # --- دکمه کاربر ---
    try:
        profile_icon = PhotoImage(file="person.png")
        profile_btn = tk.Button(
            buttons_frame,
            image=profile_icon,
            bg=THEME_COLOR,
            bd=0,
            highlightthickness=0,
            relief="flat",
            command=show_profile_window
        )
        profile_btn.image = profile_icon
        profile_btn.pack(side="left", padx=(5,0))
    except Exception as e:
        print(f"❌ آیکون person.png بارگذاری نشد: {e}")
        # جایگزین متنی با پس‌زمینه آبی تم
        profile_btn = tk.Button(
            buttons_frame,
            text="👤",
            font=("Arial", 14),
            bg=THEME_COLOR,
            fg="white",
            bd=0,
            highlightthickness=0,
            relief="flat",
            command=show_profile_window
        )
        profile_btn.pack(side="left", padx=5)
    try:
        cart_icon = PhotoImage(file="cart_icon.png")
        cart_btn = tk.Button(nav_bar, image=cart_icon, bg=THEME_COLOR, bd=0, command=show_cart_window)
        cart_btn.image = cart_icon
    except:
        cart_btn = tk.Button(nav_bar, text="🛒", bg=THEME_COLOR, fg="white", font=("Arial", 14), bd=0,
                             command=show_cart_window)
    cart_btn.pack(side="left", padx=(0, 5), pady=20)
    # دسته‌بندی‌ها
    tk.Label(root, text="دسته‌بندی کالاها", font=("Arial", 16, "bold"), fg=THEME_COLOR, bg=BG_COLOR).pack(pady=(10, 5))
    category_frame = tk.Frame(root, bg=BG_COLOR)
    category_frame.pack(pady=10)
    # --- باز کردن بنر ها ---
    def open_banner_page(title):
        new_window = tk.Toplevel(root)
        new_window.title(title)
        new_window.geometry("400x200")
        tk.Label(new_window, text=f"این {title} است", font=("Vazirmatn", 14)).pack(expand=True)
    # --- بنر اول ---
    try:
        banner1_image = PhotoImage(file="banner1.png")
        banner1_button = tk.Button(root, image=banner1_image, bd=0, bg='white',
                                   command=lambda: show_category_products("دیجیتال"))
        banner1_button.image = banner1_image
        banner1_button.place(x=50, y=407)
    except:
        print("تصویر بنر 1 یافت نشد")
    # --- بنر دوم ---
    try:
        banner2_image = PhotoImage(file="banner2.png")
        banner2_button = tk.Button(root, image=banner2_image, bd=0, bg='white',
                                   command=lambda: show_category_products("لپ‌تاپ"))
        banner2_button.image = banner2_image
        banner2_button.place(x=503, y=407)
    except:
        print("تصویر بنر 2 یافت نشد")

    create_discount_bar(root)

    categories = [
        ("mobile.png", "موبایل"),
        ("laptop.png", "لپ‌تاپ"),
        ("headphone.png", "هدفون"),
        ("watch.png", "ساعت"),
        ("digital_goods.png", "دیجیتال")
    ]

    for img_file, text in categories:
        try:
            img = PhotoImage(file=img_file)
        except:
            img = None

        frame = tk.Frame(category_frame, bg=BG_COLOR)
        frame.pack(side="right", padx=10)
        btn = tk.Button(
            frame,
            image=img if img else None,
            text=text if not img else "",
            width=64,
            height=64,
            bg=BG_COLOR,
            bd=0,
            command=lambda c=text: show_category_products(c)
        )
        btn.image = img
        btn.pack()
        tk.Label(frame, text=text, bg=BG_COLOR, fg=THEME_COLOR, font=("Arial", 10)).pack()

    # --- تابع بازکردن لینک پروژه در گیت هاب ---
    def open_github():
        webbrowser.open_new("https://github.com/USERNAME/REPO")
    # --- تابع پاورقی ---
    def create_footer(parent):
        footer_frame = tk.Frame(parent, bg="#eeeeee", height=40)
        footer_frame.pack(fill="x", side="bottom")
        footer_frame.pack_propagate(False)

        separator = tk.Frame(footer_frame, bg="#cccccc", height=1)
        separator.pack(fill="x", side="top")

        content_frame = tk.Frame(footer_frame, bg="#eeeeee")
        content_frame.pack(fill="both", expand=True)

        #  ارتباط با ما
        contact_label = tk.Label(
            content_frame,
            text="ارتباط با ما",
            bg="#eeeeee",
            fg="#000000",
            font=("Segoe UI", 10, "bold")
        )
        contact_label.pack(side="right", padx=10)

        # عنوان پروژه
        right_label = tk.Label(
            content_frame,
            text="Shopera – Advanced Programming Final Project | Designed by Mobina Kalhori",
            bg="#eeeeee",
            fg="gray",
            font=("Calibri", 10, "bold")
        )
        right_label.pack(side="left", padx=15)

        #  آیکون گیت‌هاب
        try:
            github_icon = PhotoImage(file="github.png")
            github_btn = tk.Label(content_frame, image=github_icon, bg="#eeeeee", cursor="hand2")
            github_btn.image = github_icon
            github_btn.pack(side="right", padx=0)
            github_btn.bind("<Button-1>", lambda e: open_github())
        except:
            fallback_label = tk.Label(content_frame, text="GitHub", fg="blue", cursor="hand2", bg="#eeeeee")
            fallback_label.pack(side="right", padx=0)
            fallback_label.bind("<Button-1>", lambda e: open_github())

    create_footer(root)

    root.mainloop()
# ---اجرای برنامه ---

if __name__ == "__main__":
    show_logo()
    main_app()