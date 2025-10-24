📚 MyLibrary App - نظام إدارة محتوى مكتبة متقدم / Advanced Library Content Management System
English: MyLibrary App is an open-source desktop application designed for efficient management and organization of books and authors. The project aims to provide an advanced and structured Graphical User Interface (GUI) that adheres to a clear separation of logic and data layers.

العربية: تطبيق MyLibrary App هو نظام مكتبي مفتوح المصدر مصمم للإدارة والتنظيم الفعال لمجموعة الكتب والكتّاب. يهدف المشروع إلى توفير واجهة مستخدم رسومية (GUI) متقدمة ومنظمة تتبع مبدأ الفصل الواضح بين طبقات المنطق والبيانات.

⚡ Advanced Features / ميزات متقدمة: Comprehensive search, state caching, and sophisticated Tkinter GUI design.

✨ Key Features / الميزات الأساسية
Security and Authentication / الأمان والمصادقة
مصادقة عبر البريد الإلكتروني (Email Authentication - OTP): آلية تسجيل دخول آمنة، حيث يتم إرسال رمز فريد (OTP) إلى بريد المستخدم المسجل للتحقق.

Secure Secrets Management: حماية بيانات الاعتماد الحساسة (مثل كلمة مرور SMTP) باستخدام ملفات gitignore.

Data Management / إدارة البيانات
CRUD كامل: دعم عمليات الإنشاء، القراءة، التحديث، والحذف (CRUD) لكل من الكتب، الكتّاب، والتصنيفات.

ملخص الكتّاب: عرض بيانات الكتّاب مع حساب عدد الكتب المرتبطة بهم في المكتبة.

UI/UX & Performance / الواجهة والأداء
نظام التخزين المؤقت للحالة (State Caching): تخزين البيانات المجلوبة (مثل أحدث الكتب) في الذاكرة لتجنب الاستعلام المتكرر وتحسين سرعة التنقل بين الواجهات.

تصميم واجهة متقدم (Advanced GUI): يتميز بتنسيق شبكي ثابت الأبعاد لعرض البطاقات (Fixed Grid Layout) وعناوين قابلة للنقر لعرض التفاصيل.

فصل الاهتمامات (Separation of Concerns): فصل واضح بين طبقة العرض (GUI/View) وطبقة التحكم (Controller) ومنطق قاعدة البيانات (Model/DB).

💻 Architecture & Technologies / البنية والتقنيات
The system is built using the following core technologies:


تم بناء هذا النظام باستخدام التقنيات الأساسية التالية:

Python 3.x: لغة البرمجة الأساسية والتحكم بالمنطق، بما في ذلك إرسال البريد الإلكتروني عبر SMTP.

Tkinter: مكتبة الواجهات الرسومية (GUI).

MySQL / MariaDB: قاعدة البيانات الرئيسية لتخزين جميع بيانات التطبيق والمستخدمين.
