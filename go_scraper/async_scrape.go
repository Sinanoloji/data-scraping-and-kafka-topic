package main

import (
	"encoding/json"
	"fmt"
	"os"
	"time"

	"github.com/gocolly/colly"
)

type Summary struct {
	Name        string `json:"name"`
	Price       string `json:"price"`
	Description string `json:"description"`
	Stock       string `json:"stock"`
}

func main() {
	start := time.Now()
	c := colly.NewCollector(
		colly.AllowedDomains("scrapeme.live"),
		colly.Async(true),
	)

	var summaries []Summary

	c.OnHTML(".summary", func(h *colly.HTMLElement) {
		summary := Summary{
			Name:        h.ChildText("h1.product_title"),
			Price:       h.ChildText("p.price"),
			Description: h.ChildText("div.woocommerce-product-details__short-description"),
			Stock:       h.ChildText("p.stock"),
		}
		summaries = append(summaries, summary)
	})

	c.OnHTML("li.product-type-simple a.woocommerce-LoopProduct-link", func(h *colly.HTMLElement) {
		c.Visit(h.Request.AbsoluteURL(h.Attr("href")))
	})

	c.Visit("https://scrapeme.live/shop/")
	c.Wait()

	content, err := json.Marshal(summaries)

	if err != nil {
		fmt.Println(err.Error())
	}

	os.WriteFile("pokemon.json", content, 0644)
	duration := time.Since(start)
	fmt.Println(duration)
}
