## Annotation Guidlines

## Original Examples `\`

An original example is an example that hasn't been annotated before. It could be for a specific task like `Sentiment Analysis`:

```python
{
    'input': 'ماهي مشاعر الجملة التالية: الفيلم كان رائع جداً'
    'output': 'مشاعرة الجملة السابقة إيجابية'
}
```

You can take some inspirations from 50 original task templates [here](https://huggingface.co/datasets/arbml/aya_prompts).

It could be a general example:

```python
{
    'input': 'اكتب بريد إلتكروني من شركة لشكر شخص لشرائة هاتف سامسونج إس 7'
    'output': 'نأمل إن تكون قد استمتعت بشرائك الأخير لـ هاتف سامسونج إس 7 ونرجو أن ينال على إعاجبك.'
}
```

It can also in specific a dialect:

```python
{
    'input': 'اكتب إيميل من شركة عشان تشكر شخص اشترى جوال سامسونج إس 7'
    'output': 'حبينا نشكرك على شراء جوال سامسونج إس 7.'
}
```

## Fix Previous Annotations `\review`

Some examples in the original CIDAR have some issues: For example the following example should have 
an extra space in the `output`

```python
{
    'input': '"اصنع جملة باستخدام عبارة "من حين لآخر'
    'output': 'أحب أن آخذ استراحةمن حين لأخر لأريح عقلي'
}
```

## Fix Previous Annotations `\explore`

Take inspirations from previous examples.


