from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, TIMESTAMP, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy import Enum
import enum


Base = declarative_base()

class MenuItem(Base):
    __tablename__ = 'menu_items'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False, default=0)

    order_details = relationship("OrderDetails", back_populates="menu_item")

    def __repr__(self):
        return f"Menu Item(name={self.name}, price={self.price}, quantity:{self.quantity}"


class Table(Base):
    __tablename__ = 'tables'
    id = Column(Integer, primary_key=True)
    table_number = Column(Integer, nullable=False, autoincrement=True, unique=True)
    status = Column(Boolean, default=True)

    orders = relationship("Order",  back_populates="table")

    def __repr__(self):
        return f"table number: {self.table_number}, status: {'available' if self.status else 'not available'}"

#diffrent types of order status for Order model
class OrderStatus(enum.Enum):
    pending = "pending"
    done = "done"
    canceled = "canceled"


class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    table_id = Column(Integer, ForeignKey("tables.id"))
    order_time = Column(TIMESTAMP, nullable=False, default=datetime.now)
    status = Column(Enum(OrderStatus, name="order_status_enum", create_type=True), default=OrderStatus.pending)

    table = relationship("Table", back_populates="orders")
    order_details = relationship("OrderDetails", back_populates="order", cascade="all, delete-orphan")

    def __repr__(self):
        order_time_str = self.order_time.strftime("%Y-%m-%d %H:%M:%S")
        return f"order id:{self.id}, table number:{self.table.table_number}, order time:{order_time_str}"


class OrderDetails(Base):
    __tablename__ = 'order_details'
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    item_id = Column(Integer, ForeignKey("menu_items.id"))
    quantity = Column(Integer)

    order = relationship("Order", back_populates="order_details")
    menu_item = relationship("MenuItem", back_populates="order_details")