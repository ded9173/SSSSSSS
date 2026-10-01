import uuid
from datetime import date, datetime
from sqlalchemy import create_engine, Column, Integer, String, Numeric, Date, DateTime, ForeignKey, func, CheckConstraint, Boolean
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.dialects.postgresql import UUID

Base = declarative_base()

class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, nullable=False)
    name = Column(String, nullable=False)
    item_type = Column(String, nullable=False)  # 'Продукция', 'Материалы', 'Операция'
    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        CheckConstraint(
            "item_type IN ('Продукция', 'Материалы', 'Операция')",
            name="chk_item_type"
        ),
    )

    # Связи
    specifications = relationship("Specification", back_populates="item", cascade="all, delete-orphan")
    prices = relationship("Price", back_populates="item", cascade="all, delete-orphan")
    cost_prices = relationship("CostPrice", back_populates="item", cascade="all, delete-orphan")
    production_orders = relationship("ProductionOrder", back_populates="item", cascade="all, delete-orphan")
    customer_order_items = relationship("CustomerOrderItem", back_populates="item")


class Countreparty(Base):
    __tablename__ = 'countreparties'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    inn = Column(String)  # ИНН обычно строка
    address = Column(String)
    phone = Column(String)
    type = Column(String)  # 'Клиент', 'Поставщик' и т.д.
    created_at = Column(DateTime, server_default=func.now())

    orders = relationship("CustomerOrder", back_populates="countreparty", cascade="all, delete-orphan")


class CustomerOrder(Base):
    __tablename__ = 'customer_order'

    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String, unique=True, nullable=False)
    order_date = Column(Date, nullable=False)
    countreparties_id = Column(Integer, ForeignKey('countreparties.id'))
    executor_id = Column(Integer, ForeignKey('users.user_id'))  # Ссылка на пользователя
    total_amount = Column(Numeric(10, 2), default=0.0)
    created_at = Column(DateTime, server_default=func.now())

    # Связи
    countreparty = relationship("Countreparty", back_populates="orders")
    executor = relationship("User", back_populates="customer_orders")
    items = relationship("CustomerOrderItem", back_populates="order", cascade="all, delete-orphan")


class CustomerOrderItem(Base):
    __tablename__ = 'customer_order_item'

    id = Column(Integer, primary_key=True, index=True)
    customer_order_id = Column(Integer, ForeignKey('customer_order.id'))
    item_id = Column(Integer, ForeignKey('items.id'))
    quantity = Column(Numeric(10, 2), default=1.0)
    unit_price = Column(Numeric(10, 2), default=0.0)
    discount = Column(Numeric(10, 2), default=0.0)

    order = relationship("CustomerOrder", back_populates="items")
    item = relationship("Item", back_populates="customer_order_items")


class Price(Base):
    __tablename__ = 'price'

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey('items.id'))
    price = Column(Numeric(10, 2), nullable=False)
    effective_date = Column(Date, nullable=False, default=date.today)

    item = relationship("Item", back_populates="prices")
    cost_prices = relationship("CostPrice", back_populates="price", cascade="all, delete-orphan")


class CostPrice(Base):
    __tablename__ = 'cost_price'

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey('items.id'))
    price_id = Column(Integer, ForeignKey('price.id'))
    cost_price = Column(Numeric(10, 2), nullable=False)

    item = relationship("Item", back_populates="cost_prices")
    price = relationship("Price", back_populates="cost_prices")


class ProductionOrder(Base):
    __tablename__ = 'production_orders'

    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String(50), unique=True, nullable=False)
    order_date = Column(Date, nullable=False)
    subdivision = Column(String(100))
    status = Column(String(20), nullable=False, server_default='Новый')
    item_id = Column(Integer, ForeignKey('items.id'))  # Связь с продукцией
    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        CheckConstraint(
            "status IN ('Новый', 'В работе', 'Завершён', 'Отменён')",
            name="chk_production_status"
        ),
    )

    item = relationship("Item", back_populates="production_orders")


class Specification(Base):
    __tablename__ = 'specifications'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    item_id = Column(Integer, ForeignKey('items.id'))  # Продукция, для которой спецификация
    material_id = Column(Integer, ForeignKey('items.id'))  # Материал или операция
    quantity = Column(Numeric(10, 2))
    operation_time = Column(Numeric(10, 2))  # Для операций

    item = relationship("Item", foreign_keys=[item_id], back_populates="specifications")
    material = relationship("Item", foreign_keys=[material_id])


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    login = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False, server_default="Пользователь")
    is_blocked = Column(Boolean, nullable=False, server_default="false")
    failed_attempts = Column(Integer, nullable=False, server_default="0")
    blocked_until = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        CheckConstraint(
            "role IN ('Администратор', 'Пользователь')",
            name="chk_user_role"
        ),
    )

    notes = relationship("Note", back_populates="user")
    customer_orders = relationship("CustomerOrder", back_populates="executor")

    # Свойства для Flask-Login
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return not self.is_blocked

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.user_id)


class Note(Base):
    __tablename__ = 'notes'

    note_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    content = Column(String, nullable=False)
    id_user = Column(Integer, ForeignKey("users.user_id"), nullable=False, index=True)
    created_at = Column(DateTime, server_default=func.now())

    user = relationship("User", back_populates="notes")