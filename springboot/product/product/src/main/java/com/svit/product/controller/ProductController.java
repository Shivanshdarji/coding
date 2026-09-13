package com.svit.product.controller;

import com.svit.product.entity.Product;
import com.svit.product.service.ProductService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ProductController {

    @Autowired
    private ProductService productService;

    @PostMapping("/save")
    public String saveProduct(@RequestBody Product product) {
        productService.add(product);
        return "product inserted.";
    }
}