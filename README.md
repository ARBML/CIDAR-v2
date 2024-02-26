# 🌴CIDAR v2
<p align="center">
<img src="https://cdn-uploads.huggingface.co/production/uploads/655e10b1c38270696b290f20/lKec96otC8VdM09SnPKL8.png" width = "150px"/>
</p>

CIDAR-v2: Culturally-Relevant Instruction Dataset For Arabic v2. We need to fix the issues of the previous version and also add more samples. 

## 📝 CIDAR Annotation

Our data annotation paltform was built on top of flask library. You can follow the next steps to run the app. 

### ⚡️To Run The App:
1. Install the requirements `pip install -r requirements.txt`.
2. Run the app using flask `flask --app app run `.

### ✨ Demo

 Reviewers can make changes on `Instruction` and `Output` to add new samples or review the previous samples from CIDAR. 

`instruction(str)`: required instruction. Each of the 10K instructions is reviewd by a contributer.

`output(str)`: response for the instruction given.


## 📄 Sample From The Dataset:
This sample shows an Arabic-specific intruction which related to `البلاغة` and `الإعراب`. The sentence is orignally in Arabic - not translated from any other lanaguage - 

 `index`: 10030

 `instruction`: لو سمحت اين صيغة المبالغة في " الجاحظ اديب سيارة اراؤه" و ما اعراب الجملة؟

 `output`:
 
           'صيغة المبالغة في هذه الجملة هي "سيّارة"، فاسم الفاعل من "السير" هو '
           '"سائر/ سائرة" وإذا أردت الدلالة على المبالغة في سير الآراء (أي '
           'شهرتها وكثرة تداولها) قلت "آراء سيّارة".\r\n'
           'أما إعراب الجملة فهو: "الجاحظُ": مبتدأ مرفوع بالضمة. "أديبٌ": خبر '
           'مرفوع بالضمة. "سيارةٌ": خبر متقدم، و"آراؤُه": مبتدأ متأخر، وهو '
           'مضاف والهاء ضمير متصل مضاف إليه في محل جر.  ويمكن اعتبار "سيارة" '
           'مبتدأ وهو وصف يعمل عمل فعله، و"آراؤُه" فاعل سدّ مسدّ الخبر.\r\n'
           'وفي الحالتين فجملة "سيارة آراؤه" جملة اسمية في محل رفع نعت '
           'لـ"أديب".'

## 📉 Statistics

...

## ⛔️ Limitations and Future Work

...

## 🧩 Contributers

...

## 🔑 License

...
