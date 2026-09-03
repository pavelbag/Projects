DELETE FROM auth_user;
DELETE FROM news_author;
DELETE FROM news_category;
DELETE FROM news_comment;
DELETE FROM news_post;
DELETE FROM news_postcategory;

DELETE FROM sqlite_sequence WHERE name='auth_user';
DELETE FROM sqlite_sequence WHERE name='news_author';
DELETE FROM sqlite_sequence WHERE name='news_category';
DELETE FROM sqlite_sequence WHERE name='news_comment';
DELETE FROM sqlite_sequence WHERE name='news_post';
DELETE FROM sqlite_sequence WHERE name='news_postcategory';