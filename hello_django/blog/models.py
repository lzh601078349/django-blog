
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.utils.html import strip_tags
import markdown


class Category(models.Model):
    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name

    objects = models.Manager()
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Tag(models.Model):
    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    objects = models.Manager()
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):
    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']

    objects = models.Manager()
    title = models.CharField("标题", max_length=70)
    body = models.TextField("正文")
    created_time = models.DateTimeField("创建时间", default=timezone.now)
    modified_time = models.DateTimeField("修改时间")
    excerpt = models.CharField("摘要", max_length=200, blank=True)
    tags = models.ManyToManyField(Tag, verbose_name="标签",  blank=True)
    category = models.ForeignKey(
        Category, verbose_name="分类",  on_delete=models.CASCADE)
    author = models.ForeignKey(
        User, verbose_name="作者", on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.modified_time = timezone.now()

        # 首先实例化一个 Markdown 类，用于渲染 body 的文本。
        # 由于摘要并不需要生成文章目录，所以去掉了目录拓展。
        md = markdown.Markdown(extensions=[
            # extra 本身包含很多基础拓展，而 codehilite 是语法高亮拓展，
            # 这为后面的实现代码高亮功能提供基础，而 toc 则允许自动生成目录
            "markdown.extensions.extra", "markdown.extensions.codehilite",
        ])
        # 先将 Markdown 文本渲染成 HTML 文本
        # strip_tags 去掉 HTML 文本的全部 HTML 标签
        # 从文本摘取前 54 个字符赋给 excerpt
        self.excerpt = strip_tags(md.convert(self.body))[:54]
        super().save(*args, **kwargs)
    """
第二种方法是使用 truncatechars 模板过滤器（Filter）。在 django 的模板系统中，模板过滤器的使用语法为 {{ var | filter: arg }}。
可以将模板过滤看做一个函数，它会作用于被它过滤的模板变量，从而改变模板变量的值。例如这里的 truncatechars 过滤器可以截取模板变量值
的前 N 个字符显示。关于模板过滤器，我们之前使用过 safe 过滤器，例如摘要效果，需要显示 post.body 的前 54 的字符，
那么可以在模板中使用 {{ post.body | truncatechars:54 }}。
例：<div class="entry-content clearfix">
      <p>{{ post.body|truncatechars:54 }}</p>
      <div class="read-more cl-effect-14">
          <a href="{{ post.get_absolute_url }}" class="more-link">继续阅读 <span class="meta-nav">→</span></a>
      </div>
  </div>
不过这种方法的一个缺点就是如果前 54 个字符含有块级 HTML 元素标签的话（比如一段代码块），会使摘要比较难看(无法去除HTML的标签，
在第一种方法中，使用strip_tags函数可以去除标签）。所以推荐使用第一种方法。
    """

    def get_absolute_url(self):
        return reverse("blog:detail", kwargs={"pk": self.pk})

    def __str__(self):

        return self.title
# Create your models here.
