import graphlab
# Limit number of worker processes. This preserves system memory, which prevents hosted notebooks from crashing.
graphlab.set_runtime_config('GRAPHLAB_DEFAULT_NUM_PYLAMBDA_WORKERS', 4)
#import eCommerce items Data
foods = graphlab.SFrame.read_csv('C:\Users\Jihed Mestiri\Desktop\Reviews.csv')
foods.head()
#count the words in each item description
foods['word_count'] = graphlab.text_analytics.count_words(foods['Text'])
tfidf = graphlab.text_analytics.tf_idf(foods['word_count'])
foods['tfidf'] = tfidf
#set positive sentiment starting from score >=4
foods['sentiment'] = foods['Score'] >= 4
#train the classifier
train_data,test_data = foods.random_split(.8, seed=0)
sentiment_model = graphlab.logistic_classifier.create(train_data,
                                                     target='sentiment',
                                                     features=['word_count'],
                                                     validation_set=test_data)
sentiment_model.evaluate(test_data, metric='roc_curve')
sentiment_model.show(view='Evaluation')
#train model using item similarity which allows personalization
personalized_model = graphlab.item_similarity_recommender.create(train_data, user_id='UserId', item_id='ProductId')
#make recommendations
users = foods['UserId'].unique()
personalized_model.recommend(users=users[0])
personalized_model.recommend(users=users[1])
personalized_model.recommend(users=users[2])