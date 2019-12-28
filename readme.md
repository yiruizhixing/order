## flask_sqlacodegen
flask-sqlacodegen 'mysql://root:123456@127.0.0.1/food_db' --tables app_access_log --outfile "common/models/log/AppAccesslog.py"  --flask

flask-sqlacodegen 'mysql://root:123456@127.0.0.1/food_db' --tables app_error_log --outfile "common/models/log/AppErrorlog.py"  --flask

flask-sqlacodegen 'mysql://root:123456@127.0.0.1/food_db' --tables food --outfile "common/models/food/Food.py"  --flask
flask-sqlacodegen 'mysql://root:123456@127.0.0.1/food_db' --tables food_cat --outfile "common/models/food/FoodCat.py"  --flask
flask-sqlacodegen 'mysql://root:123456@127.0.0.1/food_db' --tables food_sale_change_log --outfile "common/models/food/FoodSaleChangeLog.py"  --flask
flask-sqlacodegen 'mysql://root:123456@127.0.0.1/food_db' --tables food_stock_change_log --outfile "common/models/food/foodStockChangeLog.py"  --flask