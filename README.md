📚 MyLibrary App - نظام إدارة محتوى مكتبة متقدم
 MyLibrary App is an open-source desktop application for efficient management of books and authors. It features an advanced Tkinter GUI that adheres to a clear Separation of Concerns between the logic and presentation layers.
---

ا تطبيق MyLibrary App هو نظام مكتبي مفتوح المصدر مصمم للإدارة والتنظيم الفعال لمجموعة الكتب والكتّاب. يتميز بواجهة Tkinter متقدمة تتبع مبدأ الفصل الواضح بين طبقات المنطق والعرض.
---
🚀 الميزات الرئيسية (Key Features)
🛡️ الأمان والمصادقة (Authentication):

مصادقة عبر البريد الإلكتروني (Email OTP): آلية تسجيل دخول آمنة، حيث يتم إرسال رمز فريد (OTP) إلى بريد المستخدم المسجل للتحقق.

إدارة آمنة للبيانات السرية (Secrets): يتم التعامل مع كلمات مرور SMTP وبيانات الاعتماد الحساسة بأمان عبر ملفات .gitignore.

🗃️ إدارة البيانات (Data Management - Full CRUD):

CRUD كامل للكتب والكتّاب: دعم عمليات الإنشاء، القراءة، التحديث، والحذف (CRUD) على جميع الأصناف.

نظام الكتّاب المتقدم: عرض بيانات الكتّاب مع حساب عدد الكتب المرتبطة بهم في المكتبة (باستخدام استعلامات التجميع).

✨ الواجهة والأداء (UI/UX & Performance):

تخزين مؤقت للحالة (State Caching): تخزين البيانات المجلوبة مؤقتًا في الذاكرة لتجنب الاستعلام المتكرر وتحسين سرعة التنقل.

تصميم GUI احترافي: واجهة متقدمة باستخدام Tkinter تتميز بعرض البطاقات في تنسيق شبكي ثابت الأبعاد (Fixed Grid Layout) وعناوين قابلة للنقر لعرض التفاصيل.

فصل الاهتمامات (SoC): هيكل المشروع يفصل بوضوح بين طبقة الـ View (الواجهة)، الـ Controller (التحكم)، والـ Model (البيانات).

---
💻 البنية والتقنيات (Tech Stack)التقنية 
Python , Tkinter ,MySQL / MariaDB
