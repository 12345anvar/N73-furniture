import os
import shutil

from django.conf import settings
from django.core.management.base import BaseCommand

from products.models import (
    ProductCategory, ProductTag, ProductColor,
    Manufacture, Product, ProductImage, ProductColorQuantity
)


class Command(BaseCommand):
    help = "Seed the database with sample furniture products"

    ASSETS_IMG_DIR = os.path.join(settings.BASE_DIR, "assets", "img", "product")

    def copy_image_to_media(self, filename, upload_to):
        """Copy an image from assets to media and return the relative media path."""
        src = os.path.join(self.ASSETS_IMG_DIR, filename)
        if not os.path.exists(src):
            self.stdout.write(self.style.WARNING(f"Image not found: {src}"))
            return None
        dest_dir = os.path.join(str(settings.MEDIA_ROOT), upload_to)
        os.makedirs(dest_dir, exist_ok=True)
        dest = os.path.join(dest_dir, filename)
        shutil.copy2(src, dest)
        return os.path.join(upload_to, filename)

    def handle(self, *args, **options):
        self.stdout.write("🪑 Seeding furniture products...")

        # ── Categories ──
        categories_data = [
            {"name": "Living Room", "icon": "fa fa-couch", "children": [
                {"name": "Sofas", "icon": "fa fa-couch"},
                {"name": "Coffee Tables", "icon": "fa fa-table"},
                {"name": "TV Stands", "icon": "fa fa-tv"},
            ]},
            {"name": "Bedroom", "icon": "fa fa-bed", "children": [
                {"name": "Beds", "icon": "fa fa-bed"},
                {"name": "Wardrobes", "icon": "fa fa-door-closed"},
                {"name": "Nightstands", "icon": "fa fa-archive"},
            ]},
            {"name": "Kitchen & Dining", "icon": "fa fa-utensils", "children": [
                {"name": "Dining Tables", "icon": "fa fa-table"},
                {"name": "Dining Chairs", "icon": "fa fa-chair"},
                {"name": "Kitchen Cabinets", "icon": "fa fa-archive"},
            ]},
            {"name": "Office", "icon": "fa fa-briefcase", "children": [
                {"name": "Office Desks", "icon": "fa fa-desktop"},
                {"name": "Office Chairs", "icon": "fa fa-chair"},
                {"name": "Bookshelves", "icon": "fa fa-book"},
            ]},
        ]

        category_map = {}
        for cat_data in categories_data:
            parent, _ = ProductCategory.objects.get_or_create(
                name=cat_data["name"],
                defaults={"icon": cat_data["icon"]}
            )
            category_map[cat_data["name"]] = parent
            for child_data in cat_data.get("children", []):
                child, _ = ProductCategory.objects.get_or_create(
                    name=child_data["name"],
                    parent=parent,
                    defaults={"icon": child_data["icon"]}
                )
                category_map[child_data["name"]] = child

        self.stdout.write(self.style.SUCCESS(f"  ✅ Categories: {len(category_map)}"))

        # ── Tags ──
        tags_data = [
            "New Arrival", "Best Seller", "Eco-Friendly", "Handmade",
            "Premium", "Modern", "Classic", "Minimalist",
            "Luxury", "Compact", "Foldable", "Ergonomic",
        ]
        tag_map = {}
        for tag_name in tags_data:
            tag, _ = ProductTag.objects.get_or_create(name=tag_name)
            tag_map[tag_name] = tag

        self.stdout.write(self.style.SUCCESS(f"  ✅ Tags: {len(tag_map)}"))

        # ── Colors ──
        colors_data = [
            ("Walnut Brown", "#5C4033"),
            ("Oak Natural", "#C8A96E"),
            ("Charcoal Gray", "#36454F"),
            ("Ivory White", "#FFFFF0"),
            ("Midnight Black", "#1A1A2E"),
            ("Honey Maple", "#D4A76A"),
            ("Cherry Red", "#7B2D26"),
            ("Espresso Dark", "#3C1414"),
            ("Ash Gray", "#B2BEB5"),
            ("Teak Gold", "#B8860B"),
        ]
        color_map = {}
        for name, hex_code in colors_data:
            color, _ = ProductColor.objects.get_or_create(
                name=name,
                defaults={"hex_code": hex_code}
            )
            color_map[name] = color

        self.stdout.write(self.style.SUCCESS(f"  ✅ Colors: {len(color_map)}"))

        # ── Manufacturers ──
        manufacturers_data = [
            {"name": "IKEA", "country": "Sweden", "description": "Swedish-founded multinational that designs and sells ready-to-assemble furniture.", "website": "https://www.ikea.com"},
            {"name": "Ashley Furniture", "country": "United States", "description": "America's largest home furniture manufacturer and retailer.", "website": "https://www.ashleyfurniture.com"},
            {"name": "Pottery Barn", "country": "United States", "description": "Premium American home furnishing retailer.", "website": "https://www.potterybarn.com"},
            {"name": "Nieri", "country": "Italy", "description": "Italian luxury sofa and armchair manufacturer.", "website": "https://www.nfrniture.it"},
            {"name": "Hülsta", "country": "Germany", "description": "German premium furniture manufacturer known for quality craftsmanship.", "website": "https://www.huelsta.com"},
        ]
        mfr_map = {}
        for mfr_data in manufacturers_data:
            mfr, _ = Manufacture.objects.get_or_create(
                name=mfr_data["name"],
                defaults={
                    "country": mfr_data["country"],
                    "description": mfr_data["description"],
                    "website": mfr_data["website"],
                }
            )
            mfr_map[mfr_data["name"]] = mfr

        self.stdout.write(self.style.SUCCESS(f"  ✅ Manufacturers: {len(mfr_map)}"))

        # ── Products ──
        # Each product: main_image, 4 gallery images, categories, tags, color_quantities
        products_data = [
            {
                "name": "Modern L-Shape Sofa",
                "sku": "FRN-SOF-001",
                "description": "A spacious L-shaped sofa perfect for modern living rooms. Upholstered in premium fabric with high-density foam cushions for ultimate comfort.",
                "short_description": "Spacious L-shape sofa with premium fabric upholstery",
                "main_image": "1.jpg",
                "gallery": ["2.jpg", "3.jpg", "4.jpg", "5.jpg"],
                "price_uzs": 12500000, "price_usd": 980, "price_rub": 89000,
                "discount_price_uzs": 10900000, "discount_price_usd": 850, "discount_price_rub": 78000,
                "manufacture": "Nieri",
                "categories": ["Living Room", "Sofas"],
                "tags": ["Best Seller", "Modern", "Premium"],
                "colors": [("Charcoal Gray", 5), ("Ivory White", 3), ("Midnight Black", 8)],
                "is_featured": True,
            },
            {
                "name": "Scandinavian Coffee Table",
                "sku": "FRN-TBL-002",
                "description": "Minimalist Scandinavian-style coffee table made of solid oak wood with tapered legs and a natural finish.",
                "short_description": "Solid oak minimalist coffee table",
                "main_image": "6.jpg",
                "gallery": ["7.jpg", "8.jpg", "9.jpg", "10.jpg"],
                "price_uzs": 3200000, "price_usd": 250, "price_rub": 23000,
                "manufacture": "IKEA",
                "categories": ["Living Room", "Coffee Tables"],
                "tags": ["Minimalist", "Eco-Friendly", "New Arrival"],
                "colors": [("Oak Natural", 15), ("Walnut Brown", 10)],
                "is_featured": True,
            },
            {
                "name": "King Size Platform Bed",
                "sku": "FRN-BED-003",
                "description": "Elegant king-size platform bed with an upholstered headboard. Solid wood frame ensures durability and stability for years.",
                "short_description": "King-size platform bed with upholstered headboard",
                "main_image": "11.jpg",
                "gallery": ["12.jpg", "13.jpg", "14.jpg", "15.jpg"],
                "price_uzs": 18900000, "price_usd": 1480, "price_rub": 135000,
                "discount_price_uzs": 16500000, "discount_price_usd": 1290, "discount_price_rub": 118000,
                "manufacture": "Hülsta",
                "categories": ["Bedroom", "Beds"],
                "tags": ["Luxury", "Premium", "Classic"],
                "colors": [("Walnut Brown", 4), ("Espresso Dark", 6), ("Midnight Black", 2)],
                "is_featured": True,
            },
            {
                "name": "Sliding Door Wardrobe",
                "sku": "FRN-WRD-004",
                "description": "Spacious sliding door wardrobe with mirrored front panel. Internal compartments include shelves, drawers, and a hanging rail.",
                "short_description": "Sliding door wardrobe with mirror and internal drawers",
                "main_image": "16.jpg",
                "gallery": ["17.jpg", "18.jpg", "20.jpg", "22.jpg"],
                "price_uzs": 9800000, "price_usd": 770, "price_rub": 70000,
                "manufacture": "IKEA",
                "categories": ["Bedroom", "Wardrobes"],
                "tags": ["Modern", "Compact"],
                "colors": [("Ivory White", 7), ("Oak Natural", 5), ("Ash Gray", 3)],
                "is_featured": False,
            },
            {
                "name": "Extendable Dining Table",
                "sku": "FRN-DIN-005",
                "description": "Solid wood extendable dining table that seats 6 to 10 people. Perfect for family gatherings and dinner parties.",
                "short_description": "Extendable solid wood dining table for 6-10 people",
                "main_image": "23.jpg",
                "gallery": ["24.jpg", "25.jpg", "26.jpg", "27.jpg"],
                "price_uzs": 7600000, "price_usd": 595, "price_rub": 54000,
                "manufacture": "Ashley Furniture",
                "categories": ["Kitchen & Dining", "Dining Tables"],
                "tags": ["Classic", "Best Seller", "Handmade"],
                "colors": [("Walnut Brown", 8), ("Cherry Red", 4), ("Teak Gold", 6)],
                "is_featured": True,
            },
            {
                "name": "Ergonomic Office Chair",
                "sku": "FRN-CHR-006",
                "description": "High-back ergonomic office chair with lumbar support, adjustable armrests, headrest, and breathable mesh back.",
                "short_description": "Ergonomic mesh office chair with lumbar support",
                "main_image": "28.jpg",
                "gallery": ["29.jpg", "30.jpg", "31.jpg", "32.jpg"],
                "price_uzs": 4500000, "price_usd": 350, "price_rub": 32000,
                "discount_price_uzs": 3800000, "discount_price_usd": 299, "discount_price_rub": 27000,
                "manufacture": "Ashley Furniture",
                "categories": ["Office", "Office Chairs"],
                "tags": ["Ergonomic", "Modern", "Best Seller"],
                "colors": [("Midnight Black", 12), ("Charcoal Gray", 7)],
                "is_featured": True,
            },
            {
                "name": "Wooden Bookshelf",
                "sku": "FRN-BSH-007",
                "description": "Tall 5-tier open bookshelf crafted from solid pine wood. Ideal for living rooms, offices, and study areas.",
                "short_description": "5-tier solid pine wood open bookshelf",
                "main_image": "33.jpg",
                "gallery": ["34.jpg", "1.jpg", "2.jpg", "3.jpg"],
                "price_uzs": 2900000, "price_usd": 225, "price_rub": 21000,
                "manufacture": "IKEA",
                "categories": ["Office", "Bookshelves"],
                "tags": ["Minimalist", "Eco-Friendly", "Compact"],
                "colors": [("Oak Natural", 20), ("Honey Maple", 12), ("Walnut Brown", 9)],
                "is_featured": False,
            },
            {
                "name": "Leather Recliner Sofa",
                "sku": "FRN-RCL-008",
                "description": "Luxurious 3-seater leather recliner sofa with power reclining mechanism and built-in USB ports.",
                "short_description": "3-seater leather recliner with power mechanism",
                "main_image": "4.jpg",
                "gallery": ["5.jpg", "6.jpg", "7.jpg", "8.jpg"],
                "price_uzs": 22000000, "price_usd": 1720, "price_rub": 157000,
                "manufacture": "Nieri",
                "categories": ["Living Room", "Sofas"],
                "tags": ["Luxury", "Premium"],
                "colors": [("Espresso Dark", 3), ("Midnight Black", 5), ("Cherry Red", 2)],
                "is_featured": True,
            },
            {
                "name": "Velvet Dining Chair Set",
                "sku": "FRN-DCH-009",
                "description": "Set of 4 velvet upholstered dining chairs with gold-finished metal legs. Adds elegance to any dining setup.",
                "short_description": "Set of 4 velvet dining chairs with gold legs",
                "main_image": "9.jpg",
                "gallery": ["10.jpg", "11.jpg", "12.jpg", "13.jpg"],
                "price_uzs": 5400000, "price_usd": 420, "price_rub": 38000,
                "manufacture": "Pottery Barn",
                "categories": ["Kitchen & Dining", "Dining Chairs"],
                "tags": ["Modern", "Luxury", "New Arrival"],
                "colors": [("Charcoal Gray", 10), ("Ivory White", 6), ("Teak Gold", 4)],
                "is_featured": False,
            },
            {
                "name": "Executive Office Desk",
                "sku": "FRN-DSK-010",
                "description": "Large executive office desk with 3 drawers, cable management system, and a solid wood top with metal frame.",
                "short_description": "Executive desk with drawers and cable management",
                "main_image": "14.jpg",
                "gallery": ["15.jpg", "16.jpg", "17.jpg", "18.jpg"],
                "price_uzs": 8200000, "price_usd": 640, "price_rub": 59000,
                "discount_price_uzs": 7100000, "discount_price_usd": 555, "discount_price_rub": 51000,
                "manufacture": "Hülsta",
                "categories": ["Office", "Office Desks"],
                "tags": ["Premium", "Classic", "Ergonomic"],
                "colors": [("Walnut Brown", 6), ("Midnight Black", 4), ("Ash Gray", 8)],
                "is_featured": True,
            },
            {
                "name": "Compact TV Stand",
                "sku": "FRN-TVS-011",
                "description": "Modern compact TV stand with open shelves and closed cabinets. Fits TVs up to 65 inches.",
                "short_description": "Modern TV stand with shelves for up to 65\" TVs",
                "main_image": "20.jpg",
                "gallery": ["22.jpg", "23.jpg", "24.jpg", "25.jpg"],
                "price_uzs": 3800000, "price_usd": 295, "price_rub": 27000,
                "manufacture": "IKEA",
                "categories": ["Living Room", "TV Stands"],
                "tags": ["Modern", "Compact", "Minimalist"],
                "colors": [("Midnight Black", 9), ("Oak Natural", 11), ("Ivory White", 5)],
                "is_featured": False,
            },
            {
                "name": "Bedside Nightstand",
                "sku": "FRN-NGT-012",
                "description": "Elegant bedside nightstand with 2 drawers and an open shelf. Solid wood construction with soft-close drawer mechanism.",
                "short_description": "Solid wood nightstand with 2 drawers",
                "main_image": "26.jpg",
                "gallery": ["27.jpg", "28.jpg", "29.jpg", "30.jpg"],
                "price_uzs": 1800000, "price_usd": 140, "price_rub": 13000,
                "manufacture": "Pottery Barn",
                "categories": ["Bedroom", "Nightstands"],
                "tags": ["Classic", "Handmade", "Eco-Friendly"],
                "colors": [("Honey Maple", 14), ("Walnut Brown", 10), ("Espresso Dark", 7)],
                "is_featured": False,
            },
        ]

        created_count = 0
        for p_data in products_data:
            if Product.objects.filter(sku=p_data["sku"]).exists():
                self.stdout.write(f"  ⏭️  Skipping {p_data['sku']} — already exists")
                continue

            # Copy main image
            main_img_path = self.copy_image_to_media(p_data["main_image"], "product_images")

            product = Product.objects.create(
                name=p_data["name"],
                sku=p_data["sku"],
                description=p_data["description"],
                short_description=p_data["short_description"],
                image=main_img_path or "",
                price_uzs=p_data["price_uzs"],
                price_usd=p_data["price_usd"],
                price_rub=p_data["price_rub"],
                discount_price_uzs=p_data.get("discount_price_uzs"),
                discount_price_usd=p_data.get("discount_price_usd"),
                discount_price_rub=p_data.get("discount_price_rub"),
                manufacture=mfr_map[p_data["manufacture"]],
                is_featured=p_data.get("is_featured", False),
            )

            # Categories
            for cat_name in p_data["categories"]:
                product.categories.add(category_map[cat_name])

            # Tags
            for tag_name in p_data["tags"]:
                product.tags.add(tag_map[tag_name])

            # Color quantities
            for color_name, qty in p_data["colors"]:
                ProductColorQuantity.objects.create(
                    product=product,
                    color=color_map[color_name],
                    quantity=qty,
                )

            # Gallery images (4 images)
            for idx, img_filename in enumerate(p_data["gallery"]):
                img_path = self.copy_image_to_media(img_filename, "product_images")
                if img_path:
                    ProductImage.objects.create(
                        product=product,
                        image=img_path,
                        alt_text=f"{p_data['name']} — image {idx + 1}",
                        is_primary=(idx == 0),
                        order=idx + 1,
                    )

            created_count += 1
            self.stdout.write(f"  ✅ Created: {product.name} (SKU: {product.sku})")

        self.stdout.write(self.style.SUCCESS(
            f"\n🎉 Done! Created {created_count} products "
            f"({Product.objects.count()} total in DB)."
        ))

