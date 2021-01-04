use test
set names utf8;

-- 1. Выбрать все товары (все поля)
select * from product

-- 2. Выбрать названия всех автоматизированных складов
select name from store where store.is_automated=1

-- 3. Посчитать общую сумму в деньгах всех продаж
select sum(total) from sale

-- 4. Получить уникальные store_id всех складов, с которых была хоть одна продажа
select DISTINCT store_id from sale


-- 5. Получить уникальные store_id всех складов, с которых не было ни одной продажи
select DISTINCT store_id from store left join sale using(store_id) where sale.store_id is null

-- 6. Получить для каждого товара название и среднюю стоимость единицы товара avg(total/quantity), если товар не продавался, он не попадает в отчет.
select p.name, avg(s.total/s.quantity) from sale as s join product as p using(product_id) group by product_id

-- 7. Получить названия всех продуктов, которые продавались только с единственного склада
select p.name from sale as s join product as p using(product_id) group by name having count(DISTINCT s.store_id)=1

-- 8. Получить названия всех складов, с которых продавался только один продукт
select store.name from sale join store using(store_id) group by store.name having count(distinct sale.product_id)=1

-- 9. Выберите все ряды (все поля) из продаж, в которых сумма продажи (total) максимальна (равна максимальной из всех встречающихся)
select * from sale where sale.total in (select max(sale.total) from sale)

-- 10. Выведите дату самых максимальных продаж, если таких дат несколько, то самую раннюю из них
select date from sale group by date order by sum(total) desc, date asc limit 1
