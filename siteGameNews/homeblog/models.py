from django.db import models
from django.urls import reverse
from django.db.models import Sum
from django.contrib.auth.models import User

import string


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default=0)

    def update_rating(self):
        postR = self.post_set.all().aggregate(postRating=Sum('rating'))
        p_R = 0
        p_R += postR.get('postRating')

        commentR = self.authorUser.comment_set.all().aggregate(commentRating=Sum('rating'))
        c_R = 0
        c_R += commentR.get('commentRating')

        self.ratingAuthor = p_R * 3 + c_R
        self.save()

    def __str__(self):
        return f"{self.authorUser}"


class Article(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE,  null=True, related_name="author")
    title = models.CharField(max_length=255)
    summary = models.TextField()
    full_text = models.TextField()
    category = models.CharField(max_length=255)
    pubdate = models.DateTimeField()
    slug = models.CharField(max_length=255, unique=True)
    og_image = models.ImageField(upload_to='images', null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article_page', kwargs={'slug': self.slug})

    def get_category_url(self):
        return reverse('category_page', kwargs={'category': self.category})

    def get_author_url(self):
        return reverse('author_page', kwargs={'author': self.author})

    # def censor(text, bad_words):
    #     text_list = text.split()
    #     censored_text_list = []
    #
    #     for word in text_list:
    #         clean_word = ''.join(c for c in word if c not in string.punctuation)
    #         if clean_word.lower() in bad_words:
    #             censored_word = clean_word[0] + (len(clean_word) - 1) * '*'
    #             censored_text_list.append(word.replace(clean_word, censored_word))
    #         else:
    #             censored_text_list.append(word)
    #
    #     return ' '.join(censored_text_list)
    #
    # text = "Слово прекрасное, но вот слово, со знаком препинания, не такое прекрасное!"
    # bad_words = ["слово", "прекрасное"]
    #
    # censored_text = censor(text, bad_words)
    # # С**** п*********, но вот с****, со знаком препинания, не такое п*********!