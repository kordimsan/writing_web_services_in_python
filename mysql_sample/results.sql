use test
set names utf8;

-- 1. Выбрать все товары (все поля)
select * from product;

-- 2. Выбрать названия всех автоматизированных складов
select name from store where is_automated = 1;

-- 3. Посчитать общую сумму в деньгах всех продаж
select sum(total) from sale;

-- 4. Получить уникальные store_id всех складов, с которых была хоть одна продажа
select distinct store_id from sale;

-- 5. Получить уникальные store_id всех складов, с которых не было ни одной продажи
select store_id from store where store_id not in (SELECT store_id from sale);

-- 6. Получить для каждого товара название и среднюю стоимость единицы товара avg(total/quantity), если товар не продавался, он не попадает в отчет.
select p.name, avg(total/quantity) from sale as s
inner join product as p on p.product_id = s.product_id
group by p.name;

-- 7. Получить названия всех продуктов, которые продавались только с единственного склада
select p.name from product as p
inner join sale as s on p.product_id = s.product_id
group by p.name
having COUNT(s.store_id) = 1;

-- 8. Получить названия всех складов, с которых продавался только один продукт
select p.name from store as p
inner join sale as s on p.store_id = s.store_id
group by p.name
having COUNT(s.sale_id) = 1;

-- 9. Выберите все ряды (все поля) из продаж, в которых сумма продажи (total) максимальна (равна максимальной из всех встречающихся)
select * from sale 
where total in (select MAX(total) from sale);

-- 10. Выведите дату самых максимальных продаж, если таких дат несколько, то самую раннюю из них
select date from sale where total in (select MAX(total) from sale) order by date LIMIT 1;