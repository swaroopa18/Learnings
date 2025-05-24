package it.gabrieletondi.telldontaskkata.domain;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.List;
import lombok.EqualsAndHashCode;
import lombok.ToString;

@ToString
@EqualsAndHashCode
public class Order {

  private int id;
  private OrderStatus status;
  private List<OrderItem> items;
  private String currency;
  private BigDecimal total;
  private BigDecimal tax;

  public Order(int id, OrderStatus status, List<OrderItem> items, String currency, BigDecimal total, BigDecimal tax) {
    this.id = id;
    this.status = status;
    this.items = items;
    this.currency = currency;
    this.total = total;
    this.tax = tax;
  }

  public static Order withoutOrderItems() {
    return new Order(1, new Created(), new ArrayList<>(), "EUR", new BigDecimal("0.00"), new BigDecimal("0.00"));
  }

  public boolean hasId(int orderId) {
    return id == orderId;
  }

  public void reject() {
    this.status = status.toRejected();
  }

  public void approve() {
    this.status = status.toApproved();
  }

  public void ship() {
    this.status = status.toShipped();
  }

  public void add(Product product, int quantity) {
    final OrderItem orderItem = OrderItem.forA(product, quantity);
    items.add(orderItem);
    total = orderItem.addTaxedAmountTo(total);
    tax = orderItem.addTaxAmountTo(tax);
  }

  public boolean has(OrderStatus thatStatus) {
    return status.equals(thatStatus);
  }
}
