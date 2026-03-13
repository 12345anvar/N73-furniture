import os
import shutil
from django.core.management.base import BaseCommand
from django.core.files import File
from blogs.models import Author, Category, Tag, Blog, BlogStatus


class Command(BaseCommand):
    help = 'Seed the database with fake blog data'

    BLOG_IMAGES_DIR = 'assets/img/blog'
    AUTHOR_IMAGES_DIR = 'assets/img/blog'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('Deleting existing data...'))
        Blog.objects.all().delete()
        Author.objects.all().delete()
        Tag.objects.all().delete()
        Category.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Deleted.'))

        # ── Categories ──────────────────────────────────────────────
        tech     = Category.objects.create(title_en="Technology",           title_uz="Texnologiya",            title_ru="Технологии")
        science  = Category.objects.create(title_en="Science",              title_uz="Fan",                    title_ru="Наука")
        health   = Category.objects.create(title_en="Health",               title_uz="Sog'liq",                title_ru="Здоровье")
        business = Category.objects.create(title_en="Business",             title_uz="Biznes",                 title_ru="Бизнес")
        ai       = Category.objects.create(title_en="Artificial Intelligence", title_uz="Sun'iy intellekt",    title_ru="Искусственный интеллект", parent=tech)
        webdev   = Category.objects.create(title_en="Web Development",      title_uz="Veb dasturlash",         title_ru="Веб-разработка",          parent=tech)
        nutrition= Category.objects.create(title_en="Nutrition",            title_uz="Ovqatlanish",            title_ru="Питание",                 parent=health)
        startup  = Category.objects.create(title_en="Startups",             title_uz="Startaplar",             title_ru="Стартапы",                parent=business)
        self.stdout.write(self.style.SUCCESS(f'Created {Category.objects.count()} categories.'))

        # ── Tags ─────────────────────────────────────────────────────
        tag_data = [
            ("Python",           "Python",                    "Python"),
            ("Machine Learning", "Mashinali o'rganish",       "Машинное обучение"),
            ("Django",           "Django",                    "Django"),
            ("React",            "React",                     "React"),
            ("Data Science",     "Ma'lumotlar fani",          "Наука о данных"),
            ("Cloud Computing",  "Bulutli hisoblash",         "Облачные вычисления"),
            ("Cybersecurity",    "Kiberxavfsizlik",           "Кибербезопасность"),
            ("DevOps",           "DevOps",                    "DevOps"),
            ("Blockchain",       "Blokcheyn",                 "Блокчейн"),
            ("Open Source",      "Ochiq manba",               "Открытый исходный код"),
        ]
        tags = [Tag.objects.create(title_en=en, title_uz=uz, title_ru=ru) for en, uz, ru in tag_data]
        self.stdout.write(self.style.SUCCESS(f'Created {Tag.objects.count()} tags.'))

        # ── Authors ──────────────────────────────────────────────────
        author_data = [
            (
                "Alice Johnson", "Elis Jonson", "Элис Джонсон",
                "AI researcher and tech writer with a passion for making complex topics accessible.",
                "AI tadqiqotchisi va texnik muallif.",
                "Исследователь ИИ и технический писатель.",
                "AI Researcher, Author", "AI Tadqiqotchisi, Muallif", "Исследователь ИИ, Автор",
                "user.jpg",
            ),
            (
                "Mark Stevens", "Mark Stivens", "Марк Стивенс",
                "Full-stack developer with 10 years experience building scalable web applications.",
                "10 yillik tajribaga ega full-stack dasturchi.",
                "Full-stack разработчик с 10-летним опытом.",
                "Software Engineer, Blogger", "Dasturiy muhandis, Blogger", "Инженер-программист, Блогер",
                "user1.jpg",
            ),
            (
                "Lena Müller", "Lena Myuller", "Лена Мюллер",
                "Data scientist and open source contributor who loves turning data into stories.",
                "Ma'lumotlar olimi va ochiq manba hissadori.",
                "Специалист по данным и контрибьютор open source.",
                "Data Scientist, Speaker", "Ma'lumotlar olimi, Spiker", "Специалист по данным, Спикер",
                "user2.jpg",
            ),
            (
                "Carlos Rivera", "Karlos Rivera", "Карлос Ривера",
                "Startup founder and business strategist with 3 successful exits.",
                "Startap asoschisi va biznes strateg.",
                "Основатель стартапа и бизнес-стратег.",
                "Entrepreneur, Mentor", "Tadbirkor, Mentor", "Предприниматель, Ментор",
                "user.jpg",
            ),
            (
                "Yuki Tanaka", "Yuki Tanaka", "Юки Танака",
                "Cybersecurity expert and ethical hacker helping companies stay safe online.",
                "Kiberxavfsizlik mutaxassisi va etik xaker.",
                "Эксперт по кибербезопасности и этичный хакер.",
                "Security Engineer, Researcher", "Xavfsizlik muhandisi, Tadqiqotchi", "Инженер безопасности, Исследователь",
                "user1.jpg",
            ),
        ]

        authors = []
        for d in author_data:
            author = Author(
                full_name_en=d[0], full_name_uz=d[1], full_name_ru=d[2],
                about_en=d[3],     about_uz=d[4],     about_ru=d[5],
                professions_en=d[6], professions_uz=d[7], professions_ru=d[8],
            )
            img_path = os.path.join(self.AUTHOR_IMAGES_DIR, d[9])
            if os.path.exists(img_path):
                with open(img_path, 'rb') as f:
                    author.image.save(d[9], File(f), save=False)
            author.save()
            authors.append(author)
        self.stdout.write(self.style.SUCCESS(f'Created {Author.objects.count()} authors.'))

        # ── Blogs ─────────────────────────────────────────────────────
        blog_data = [
            (
                "Getting Started with Python", "Python bilan boshlash", "Начало работы с Python",
                "Python is one of the most popular programming languages today.",
                "Python bugungi kunda eng mashhur dasturlash tillaridan biri.",
                "Python — один из самых популярных языков программирования сегодня.",
                "Python is a versatile, beginner-friendly language used in web development, data science, AI, and more. This guide walks you through setting up your environment and writing your first script.",
                "Python — ko'p qirrali, boshlang'ichlar uchun qulay til bo'lib, veb-dasturlash, ma'lumotlar fani, AI va boshqalarda qo'llaniladi.",
                "Python — универсальный язык, удобный для новичков, используемый в веб-разработке, науке о данных, ИИ и многом другом.",
                [webdev, tech], [tags[0], tags[2]], [authors[0], authors[1]], "1.jpg",
            ),
            (
                "Understanding Machine Learning", "Mashinali o'rganishni tushunish", "Понимание машинного обучения",
                "Machine learning is transforming every industry on the planet.",
                "Mashinali o'rganish har bir sohani o'zgartirmoqda.",
                "Машинное обучение трансформирует каждую отрасль.",
                "In this article, we explore the core concepts of machine learning, including supervised, unsupervised, and reinforcement learning with practical examples and Python code.",
                "Ushbu maqolada biz mashinali o'rganishning asosiy tushunchalarini ko'rib chiqamiz.",
                "В этой статье мы исследуем основные концепции машинного обучения.",
                [ai], [tags[1], tags[4]], [authors[0], authors[2]], "2.jpg",
            ),
            (
                "Building REST APIs with Django", "Django bilan REST API qurish", "Создание REST API с Django",
                "Django REST Framework makes building production-ready APIs simple.",
                "Django REST Framework API qurishni osonlashtiradi.",
                "Django REST Framework упрощает создание API.",
                "Learn how to build production-ready REST APIs using Django and Django REST Framework. We cover serializers, viewsets, authentication, permissions, and deployment best practices.",
                "Django va Django REST Framework yordamida ishlab chiqarishga tayyor REST API-larni qanday qurishni o'rganing.",
                "Узнайте, как создавать готовые к production REST API с использованием Django и Django REST Framework.",
                [webdev], [tags[2], tags[0]], [authors[1]], "3.jpg",
            ),
            (
                "React Hooks Deep Dive", "React Hooks chuqur o'rganish", "Глубокое погружение в React Hooks",
                "React Hooks revolutionized how we write React components.",
                "React Hooks React komponentlarini yozish usulimizni inqilob qildi.",
                "React Hooks произвели революцию в написании React-компонентов.",
                "This deep dive covers useState, useEffect, useContext, useReducer, and custom hooks with real-world examples and best practices.",
                "Ushbu chuqur o'rganish useState, useEffect, useContext, useReducer va maxsus hooklarni real misollar bilan qamrab oladi.",
                "Это погружение охватывает useState, useEffect, useContext, useReducer и кастомные хуки.",
                [webdev], [tags[3]], [authors[1], authors[2]], "4.jpg",
            ),
            (
                "Introduction to Data Science", "Ma'lumotlar faniga kirish", "Введение в науку о данных",
                "Data science combines statistics, programming, and domain knowledge.",
                "Ma'lumotlar fani statistika, dasturlash va soha bilimlarini birlashtiradi.",
                "Наука о данных объединяет статистику, программирование и знания предметной области.",
                "Discover the data science workflow from data collection and cleaning to visualization and modeling. Includes hands-on examples with pandas and matplotlib.",
                "Ma'lumotlar to'plash va tozalashdan tortib vizualizatsiya va modellashtrishgacha bo'lgan ma'lumotlar fani ish oqimini kashf eting.",
                "Откройте для себя рабочий процесс науки о данных от сбора и очистки данных до визуализации и моделирования.",
                [ai, science], [tags[4], tags[0]], [authors[2]], "5.jpg",
            ),
            (
                "Cloud Computing Fundamentals", "Bulutli hisoblash asoslari", "Основы облачных вычислений",
                "Cloud computing has fundamentally changed how businesses operate.",
                "Bulutli hisoblash bizneslarning ishlash usulini o'zgartirdi.",
                "Облачные вычисления изменили способ работы бизнеса.",
                "We break down IaaS, PaaS, and SaaS models, compare AWS, Azure, and GCP, and guide you through deploying your first cloud application step by step.",
                "Biz IaaS, PaaS va SaaS modellarini tahlil qilamiz, AWS, Azure va GCP ni solishtiramiz.",
                "Мы разбираем модели IaaS, PaaS и SaaS, сравниваем AWS, Azure и GCP.",
                [tech], [tags[5]], [authors[1], authors[3]], "6.jpg",
            ),
            (
                "Cybersecurity Best Practices", "Kiberxavfsizlikning eng yaxshi amaliyotlari", "Лучшие практики кибербезопасности",
                "Every developer must understand basic cybersecurity principles.",
                "Har bir dasturchi asosiy kiberxavfsizlikni tushunishi kerak.",
                "Каждый разработчик должен понимать основы кибербезопасности.",
                "From SQL injection to CSRF attacks, this article covers the OWASP Top 10 vulnerabilities and how to protect your web applications from the most common threats.",
                "SQL in'ektsiyasidan CSRF hujumlarigacha, ushbu maqola OWASP Top 10 zaifliklarni qamrab oladi.",
                "От SQL-инъекций до CSRF-атак — эта статья охватывает OWASP Top 10 уязвимостей.",
                [tech], [tags[6]], [authors[4]], "7.jpg",
            ),
            (
                "DevOps with Docker and Kubernetes", "Docker va Kubernetes bilan DevOps", "DevOps с Docker и Kubernetes",
                "Containerization has transformed software deployment forever.",
                "Konteynerizatsiya dasturiy ta'minotni joylashtirishni o'zgartirdi.",
                "Контейнеризация трансформировала развёртывание программного обеспечения.",
                "Learn how to containerize applications with Docker, orchestrate them with Kubernetes, and set up CI/CD pipelines for fully automated deployments.",
                "Ilovalarni Docker bilan konteynerlashtirish, Kubernetes bilan boshqarish va avtomatlashtirilgan joylashtirishlar uchun CI/CD pipelinelarini sozlashni o'rganing.",
                "Узнайте, как контейнеризировать приложения с Docker, оркестрировать их с Kubernetes и настраивать CI/CD пайплайны.",
                [tech], [tags[7]], [authors[1], authors[4]], "8.jpg",
            ),
            (
                "Blockchain Beyond Cryptocurrency", "Kriptovalyutadan tashqari blokcheyn", "Блокчейн за пределами криптовалюты",
                "Blockchain technology has use cases far beyond Bitcoin.",
                "Blokcheyn texnologiyasi Bitcoindan ancha uzoqda qo'llaniladi.",
                "Технология блокчейн имеет применения далеко за пределами Bitcoin.",
                "Explore how blockchain is being used in supply chain, healthcare, voting systems, and smart contracts. A practical guide to understanding distributed ledgers.",
                "Blokcheyning ta'minot zanjiri, sog'liqni saqlash, ovoz berish tizimlari va smart shartnomalarida qanday ishlatilayotganini o'rganing.",
                "Изучите, как блокчейн используется в цепочках поставок, здравоохранении, системах голосования и смарт-контрактах.",
                [tech, business], [tags[8]], [authors[3], authors[4]], "9.jpg",
            ),
            (
                "Open Source Contribution Guide", "Ochiq manbaga hissa qo'shish qo'llanmasi", "Руководство по вкладу в открытый исходный код",
                "Contributing to open source can significantly boost your career.",
                "Ochiq manbaga hissa qo'shish karerangizni rivojlantirishi mumkin.",
                "Вклад в open source может ускорить вашу карьеру.",
                "Step-by-step guide to making your first open source contribution: finding projects, understanding codebases, submitting pull requests, and handling code reviews.",
                "Birinchi ochiq manba hissangizni qo'shish bo'yicha bosqichma-bosqich qo'llanma: loyihalarni topish, pull request yuborish.",
                "Пошаговое руководство по первому вкладу в open source: поиск проектов, понимание кодовой базы, отправка pull request-ов.",
                [tech], [tags[9], tags[0]], [authors[2]], "1.jpg",
            ),
            (
                "Starting a Tech Startup in 2024", "2024-yilda texnologik startap boshlash", "Запуск технологического стартапа в 2024 году",
                "The startup landscape has evolved significantly in recent years.",
                "Startap landshafti sezilarli darajada o'zgardi.",
                "Ландшафт стартапов значительно изменился.",
                "From idea validation to finding co-founders, raising seed funding, and launching your MVP — a practical roadmap for aspiring tech entrepreneurs.",
                "G'oyani tasdiqlashdan hammuassis topishgacha, urug' moliyalashtirishni jalb qilish va MVP ni ishga tushirishgacha — amaliy yo'l xaritasi.",
                "От валидации идеи до поиска сооснователей, привлечения начального финансирования и запуска MVP — практическая дорожная карта.",
                [startup, business], [tags[8], tags[9]], [authors[3]], "2.jpg",
            ),
            (
                "The Future of Artificial Intelligence", "Sun'iy intellektning kelajagi", "Будущее искусственного интеллекта",
                "AI is advancing faster than ever before in history.",
                "AI avvalgidan tezroq rivojlanmoqda.",
                "ИИ развивается быстрее, чем когда-либо.",
                "From large language models to AGI debates, we explore where AI is headed, the ethical challenges it poses, and what it means for the future of work and society.",
                "Katta til modellaridan tortib AGI munozaralarigacha, biz AIning qayerga borayotganini o'rganamiz.",
                "От больших языковых моделей до дебатов об AGI — мы исследуем, куда движется ИИ.",
                [ai, science], [tags[1], tags[4]], [authors[0]], "3.jpg",
            ),
            (
                "Healthy Eating for Developers", "Dasturchilar uchun sog'lom ovqatlanish", "Здоровое питание для разработчиков",
                "Long coding sessions take a serious toll on your physical health.",
                "Uzoq kodlash seanslari sog'lig'ingizga ta'sir qiladi.",
                "Долгие сессии программирования сказываются на здоровье.",
                "Practical nutrition tips tailored for people with sedentary desk jobs. Covers meal prep, brain foods, hydration, and avoiding the afternoon energy crash.",
                "Sedentary ish joylari uchun moslashtirilgan amaliy ovqatlanish maslahatlari.",
                "Практические советы по питанию для людей с сидячей работой.",
                [health, nutrition], [tags[9]], [authors[2], authors[3]], "4.jpg",
            ),
            (
                "Web Security Essentials", "Veb xavfsizlik asoslari", "Основы веб-безопасности",
                "Web applications face new threats every single second.",
                "Veb-ilovalar har soniyada tahdidlarga duch keladi.",
                "Веб-приложения сталкиваются с угрозами каждую секунду.",
                "A comprehensive guide to securing web applications: HTTPS, Content Security Policy, input validation, secure cookies, and penetration testing basics every developer should know.",
                "Veb-ilovalarni himoya qilish bo'yicha to'liq qo'llanma: HTTPS, CSP, kirish ma'lumotlarini tekshirish.",
                "Подробное руководство по защите веб-приложений: HTTPS, политика безопасности контента, валидация ввода.",
                [webdev, tech], [tags[6], tags[2]], [authors[4]], "5.jpg",
            ),
            (
                "Data Visualization with Python", "Python bilan ma'lumotlarni vizualizatsiya qilish", "Визуализация данных с Python",
                "Good visualizations tell powerful, memorable stories.",
                "Yaxshi vizualizatsiyalar kuchli hikoyalarni aytib beradi.",
                "Хорошие визуализации рассказывают мощные истории.",
                "Master data visualization using matplotlib, seaborn, and plotly. Learn how to choose the right chart type and design visualizations that communicate insights clearly.",
                "Matplotlib, seaborn va plotly yordamida ma'lumotlarni vizualizatsiya qilishni o'zlashtiring.",
                "Освойте визуализацию данных с matplotlib, seaborn и plotly.",
                [ai, science], [tags[4], tags[0]], [authors[2]], "6.jpg",
            ),
            (
                "Freelancing as a Developer", "Dasturchi sifatida frilanserlik", "Фриланс как разработчик",
                "Freelancing offers freedom but comes with real challenges.",
                "Frilanserlik erkinlik beradi, lekin qiyinchiliklar bilan birga keladi.",
                "Фриланс даёт свободу, но сопряжён с трудностями.",
                "Everything you need to know about freelancing: finding clients, setting rates, managing contracts, handling taxes, and building a sustainable long-term remote career.",
                "Frilanserlik haqida bilishingiz kerak bo'lgan hamma narsa: mijozlarni topish, narxlarni belgilash.",
                "Всё, что нужно знать о фрилансе: поиск клиентов, установка ставок, управление контрактами.",
                [business, startup], [tags[9]], [authors[3]], "7.jpg",
            ),
            (
                "Understanding Neural Networks", "Neyron tarmoqlarni tushunish", "Понимание нейронных сетей",
                "Neural networks are the backbone of all modern AI systems.",
                "Neyron tarmoqlar zamonaviy AIning asosi hisoblanadi.",
                "Нейронные сети — основа современного ИИ.",
                "From perceptrons to deep learning, this article explains how neural networks work, how they learn through backpropagation, and their most impactful real-world applications.",
                "Perceptronlardan chuqur o'rganishgacha, ushbu maqola neyron tarmoqlarning qanday ishlashini tushuntiradi.",
                "От перцептронов до глубокого обучения — эта статья объясняет, как работают нейронные сети.",
                [ai], [tags[1], tags[4]], [authors[0], authors[2]], "8.jpg",
            ),
            (
                "Git and Version Control Mastery", "Git va versiyalarni boshqarishni o'zlashtirish", "Мастерство Git и контроля версий",
                "Git is the single most essential tool for every developer.",
                "Git har bir dasturchi uchun muhim vosita hisoblanadi.",
                "Git — незаменимый инструмент для каждого разработчика.",
                "Go beyond basic commits and learn Git branching strategies, rebasing, cherry-picking, resolving merge conflicts, and effective team collaboration workflows.",
                "Asosiy commitlardan tashqariga chiqing va Git tarmoqlash strategiyalarini, rebasingni o'rganing.",
                "Выйдите за рамки базовых коммитов и изучите стратегии ветвления Git, rebase, cherry-pick.",
                [webdev, tech], [tags[7], tags[9]], [authors[1]], "9.jpg",
            ),
            (
                "Nutrition Science Explained", "Ovqatlanish fanini tushuntirish", "Наука о питании объясняется",
                "Understanding nutrition science can genuinely transform your life.",
                "Ovqatlanishni tushunish hayotingizni o'zgartirishi mumkin.",
                "Понимание питания может изменить вашу жизнь.",
                "A science-based guide to macronutrients, micronutrients, gut health, intermittent fasting, and building sustainable healthy eating habits backed by current research.",
                "Makronutrientlar, mikronutrientlar, ichak salomatligi va barqaror sog'lom ovqatlanish odatlari bo'yicha ilmiy qo'llanma.",
                "Научное руководство по макронутриентам, микронутриентам, здоровью кишечника, интервальному голоданию.",
                [health, nutrition], [tags[9]], [authors[2], authors[3]], "1.jpg",
            ),
            (
                "Scaling Your SaaS Business", "SaaS biznesingizni kengaytirish", "Масштабирование вашего SaaS-бизнеса",
                "Scaling a SaaS product requires both strategy and flawless execution.",
                "SaaS ni kengaytirish strategiya va ijroni talab qiladi.",
                "Масштабирование SaaS требует стратегии и исполнения.",
                "Proven strategies for scaling a SaaS business: pricing models, churn reduction, customer success, product-led growth, and confidently expanding into new international markets.",
                "SaaS biznesini kengaytirish uchun isbotlangan strategiyalar: narxlash modellari, churnni kamaytirish.",
                "Проверенные стратегии масштабирования SaaS-бизнеса: модели ценообразования, снижение оттока.",
                [business, startup], [tags[5], tags[8]], [authors[3]], "2.jpg",
            ),
        ]

        for d in blog_data:
            blog = Blog(
                title_en=d[0],             title_uz=d[1],             title_ru=d[2],
                short_description_en=d[3], short_description_uz=d[4], short_description_ru=d[5],
                long_description_en=d[6],  long_description_uz=d[7],  long_description_ru=d[8],
                status=BlogStatus.PUBLISHED,
            )
            img_path = os.path.join(self.BLOG_IMAGES_DIR, d[12])
            if os.path.exists(img_path):
                with open(img_path, 'rb') as f:
                    blog.image.save(d[12], File(f), save=False)
            blog.save()
            blog.categories.set(d[9])
            blog.tags.set(d[10])
            blog.authors.set(d[11])

        self.stdout.write(self.style.SUCCESS(f'Created {Blog.objects.count()} blogs.'))
        self.stdout.write(self.style.SUCCESS('✅ Seeding complete!'))
        self.stdout.write(f'  Categories : {Category.objects.count()}')
        self.stdout.write(f'  Tags       : {Tag.objects.count()}')
        self.stdout.write(f'  Authors    : {Author.objects.count()}')
        self.stdout.write(f'  Blogs      : {Blog.objects.count()}')