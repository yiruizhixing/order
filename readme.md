## flask_sqlacodegen
flask-sqlacodegen 'mysql://root:123456@127.0.0.1/food_db' --tables app_access_log --outfile "common/models/log/AppAccesslog.py"  --flask

flask-sqlacodegen 'mysql://root:123456@127.0.0.1/food_db' --tables app_error_log --outfile "common/models/log/AppErrorlog.py"  --flask

flask-sqlacodegen 'mysql://root:123456@127.0.0.1/food_db' --tables food --outfile "common/models/food/Food.py"  --flask
flask-sqlacodegen 'mysql://root:123456@127.0.0.1/food_db' --tables food_cat --outfile "common/models/food/FoodCat.py"  --flask
flask-sqlacodegen 'mysql://root:123456@127.0.0.1/food_db' --tables food_sale_change_log --outfile "common/models/food/FoodSaleChangeLog.py"  --flask
flask-sqlacodegen 'mysql://root:123456@127.0.0.1/food_db' --tables food_stock_change_log --outfile "common/models/food/foodStockChangeLog.py"  --flask

flask-sqlacodegen 'mysql://root:123456@127.0.0.1/food_db' --tables images --outfile "common/models/Images.py"  --flask


flask-sqlacodegen 'mysql://root:123456@127.0.0.1/food_db' --tables xunkao_cat --outfile "common/models/Xunkao_cat.py"  --flask
flask-sqlacodegen 'mysql://root:123456@127.0.0.1/food_db' --tables people --outfile "common/models/people/People.py"  --flask

flask-sqlacodegen 'mysql://root:123456@127.0.0.1/food_db' --tables kaodian --outfile "common/models/exam/Kaodian.py"  --flask

flask-sqlacodegen 'mysql://root:123456@127.0.0.1/food_db' --tables exam --outfile "common/models/exam/Exam.py"  --flask

flask-sqlacodegen 'mysql://root:123456@127.0.0.1/food_db' --tables exam_kaowu --outfile "common/models/exam/Exam_kaowu.py"  --flask

flask-sqlacodegen 'mysql://root:123456@127.0.0.1/food_db' --tables exam_kemu --outfile "common/models/exam/Exam_kemu.py"  --flask

flask-sqlacodegen 'mysql://root:123456@127.0.0.1/food_db' --tables exam_kaodian --outfile "common/models/exam/Exam_kaodian.py"  --flask

flask-sqlacodegen 'mysql://root:123456@127.0.0.1/food_db' --tables wx_share_history --outfile "common/models/food/WxShareHistory.py"  --flask

flask-sqlacodegen 'mysql://root:123456@127.0.0.1/food_db' --tables member_cart --outfile "common/models/member/MemberCart.py"  --flask