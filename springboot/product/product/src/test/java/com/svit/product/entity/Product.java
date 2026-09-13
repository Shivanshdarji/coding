package com.svit.product.entity;

import jakarta.persistence.*;

@Entity
@Table(name = "product_details")
public class Product {
    @Id
    private Long id;

    @Column(name = "product_name")
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private String productName;

    @Column(name = "product_qty")
    private Integer qty;

    @Column(name = "product_price")
    private Integer price;

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public Integer getQty() {
        return qty;
    }

    public void setQty(Integer qty) {
        this.qty = qty;
    }

    public Integer getPrice() {
        return price;
    }

    public void setPrice(Integer price) {
        this.price = price;
    }

    public String getProductName() {
        return productName;
    }

    public void setProductName(String productName) {
        this.productName = productName;
    }
}
