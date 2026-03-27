import click
from flask.cli import AppGroup
from app.extensions import db
from app.models import User, Category, Product, Movement


def register_commands(app):
    """Register CLI commands with the Flask app."""

    @app.cli.command("seed-db")
    def seed_db():
        """Seed the database with sample data."""
        with app.app_context():
            click.echo("Seeding database...")

            admin = User.query.filter_by(username="admin").first()
            if admin:
                click.echo("Database already seeded. Skipping...")
                return

            admin = User(username="admin", email="admin@inventory.local")
            admin.set_password("admin123")
            db.session.add(admin)
            db.session.commit()

            click.echo("Created admin user: admin / admin123")

            categories_data = [
                {
                    "name": "Electrónica",
                    "description": "Dispositivos y accesorios electrónicos",
                },
                {
                    "name": "Oficina",
                    "description": "Suministros de oficina y papelería",
                },
                {"name": "Hogar", "description": "Artículos para el hogar"},
            ]

            categories = []
            for cat_data in categories_data:
                cat = Category(**cat_data)
                db.session.add(cat)
                categories.append(cat)

            db.session.commit()
            click.echo(f"Created {len(categories)} categories")

            products_data = [
                {
                    "sku": "ELEC001",
                    "name": "Laptop HP ProBook",
                    "description": 'Laptop 15.6" Intel i5',
                    "price": 899.99,
                    "stock": 15,
                    "min_stock": 5,
                    "category_id": categories[0].id,
                },
                {
                    "sku": "ELEC002",
                    "name": "Mouse Inalámbrico",
                    "description": "Mouse wireless USB",
                    "price": 29.99,
                    "stock": 50,
                    "min_stock": 10,
                    "category_id": categories[0].id,
                },
                {
                    "sku": "ELEC003",
                    "name": "Teclado Mecánico",
                    "description": "Teclado RGB gaming",
                    "price": 79.99,
                    "stock": 25,
                    "min_stock": 8,
                    "category_id": categories[0].id,
                },
                {
                    "sku": "ELEC004",
                    "name": 'Monitor 24"',
                    "description": "Monitor Full HD 24 pulgadas",
                    "price": 199.99,
                    "stock": 8,
                    "min_stock": 3,
                    "category_id": categories[0].id,
                },
                {
                    "sku": "ELEC005",
                    "name": "USB-C Hub",
                    "description": "Hub 7-en-1 USB-C",
                    "price": 49.99,
                    "stock": 30,
                    "min_stock": 10,
                    "category_id": categories[0].id,
                },
                {
                    "sku": "OFIC001",
                    "name": "Paquete de Papel A4",
                    "description": "500 hojas papel bond",
                    "price": 12.99,
                    "stock": 100,
                    "min_stock": 20,
                    "category_id": categories[1].id,
                },
                {
                    "sku": "OFIC002",
                    "name": "Bolígrafos Pack x10",
                    "description": "Bolígrafos azules",
                    "price": 8.99,
                    "stock": 5,
                    "min_stock": 15,
                    "category_id": categories[1].id,
                },
                {
                    "sku": "OFIC003",
                    "name": "Carpetas Archivadoras",
                    "description": "Carpetas tamaño carta",
                    "price": 15.99,
                    "stock": 40,
                    "min_stock": 10,
                    "category_id": categories[1].id,
                },
                {
                    "sku": "HOG001",
                    "name": "Lámpara de Escritorio",
                    "description": "Lámpara LED regulable",
                    "price": 35.99,
                    "stock": 20,
                    "min_stock": 5,
                    "category_id": categories[2].id,
                },
                {
                    "sku": "HOG002",
                    "name": "Organizador de Escritorio",
                    "description": "Portaplumas y accesorios",
                    "price": 19.99,
                    "stock": 35,
                    "min_stock": 8,
                    "category_id": categories[2].id,
                },
            ]

            products = []
            for prod_data in products_data:
                prod = Product(**prod_data)
                db.session.add(prod)
                products.append(prod)

            db.session.commit()
            click.echo(f"Created {len(products)} products")

            movements_data = [
                {
                    "product": products[0],
                    "movement_type": "entry",
                    "quantity": 15,
                    "notes": "Inventario inicial",
                },
                {
                    "product": products[1],
                    "movement_type": "entry",
                    "quantity": 50,
                    "notes": "Compra mensual",
                },
                {
                    "product": products[5],
                    "movement_type": "entry",
                    "quantity": 100,
                    "notes": "Reposición de stock",
                },
                {
                    "product": products[6],
                    "movement_type": "exit",
                    "quantity": 5,
                    "notes": "Venta directa",
                },
                {
                    "product": products[8],
                    "movement_type": "entry",
                    "quantity": 20,
                    "notes": "Inventario inicial",
                },
            ]

            for mov_data in movements_data:
                movement = Movement(
                    product_id=mov_data["product"].id,
                    user_id=admin.id,
                    movement_type=mov_data["movement_type"],
                    quantity=mov_data["quantity"],
                    notes=mov_data["notes"],
                )
                db.session.add(movement)

            db.session.commit()
            click.echo(f"Created {len(movements_data)} movements")

            click.echo("Database seeded successfully!")

    @app.cli.command("create-db")
    def create_db():
        """Create the database tables."""
        with app.app_context():
            db.create_all()
            click.echo("Database tables created!")
