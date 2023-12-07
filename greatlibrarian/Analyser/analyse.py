from ..Utils import add_logger_name_cls,generate_logger_subfile,generate_name_new
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Image as RLImage
from matplotlib.backends.backend_pdf import PdfPages
from reportlab.pdfgen import canvas
import os 
from ..Utils import extract_mistaken_info,extract_example_info
import matplotlib
import textwrap
from matplotlib.font_manager import FontProperties
from matplotlib import rcParams
import warnings


# log_name = generate_name_new('analyse')
log_name = 'analyse'
logger_name = 'analyse.log'
logger_subfile = generate_logger_subfile()
add_logger_to_class = add_logger_name_cls(log_name,os.path.join('Logs',logger_subfile))
logger_path = os.path.join(os.path.join('Logs',logger_subfile))
@add_logger_to_class
class Analyse():
    def __init__(self,score_dict) -> None:
        self.score_dict = score_dict
        self.logger_path = logger_path
    
    def analyse(self):
        """
        A function to analyse the score that LLM gets in the testproject, including many testcases.
        The information used for analysis comes from the function get_eval_result in class getinfo.
        By reading the information(a dictionary) provided by the function get_eval_result, this function will create a new log file and write the analysis in it.
        The avarage socre that the LLM gets in testcase will be recorded, and finally the function will give an overall evaluation of the LLM.
        The log file generated by this function is formatted like: 
        "By 'keywords' evaluation, the LLM gets XX(0-1) scores in average.
         By 'toolUsage' evaluation, the LLM gets XX(0-1) scores in average.
         By 'gpt4Eval' evaluation, the LLM gets XX(0-1) scores in average.
         To conclude, the LLM …"
        
        """
        score = self.score_dict
        score_list = []
        score_mean = [0]*10
        score_get = [0]*10
        field_list = ['knowledge_understanding', 'coding', 'common_knowledge', 'reasoning', 'multi_language', 'specialized_knowledge', 'traceability', 'outputformatting', 'internal_security', 'external_security']
        total_score = [0]*10

        for i in range(10):
            score_list.append(score[field_list[i]])

        for i in range(10):
            if score_list[i] == []:
                score_mean[i] = 'Not evaluated in this field'
            else:
                score_mean[i] = float('%.3f'%(sum(score_list[i])/len(score_list[i])))
                total_score[i] = (len(score_list[i]))
                score_get[i] = float('%.3f'%(sum(score_list[i])))
        get_score_info=''

        for i in range (10):
            get_score_info += f'\nIn {field_list[i]} field, the LLM gets "{score_get[i]}/{total_score[i]}" scores.\n'

        plotinfo = [field_list,score_get,total_score]

        mean_score_list=[]
        for score in score_mean:
            if score!='Not evaluated in this field':
                if score>=0.6:
                    mean_score_list.append('does well in')
                else:
                    mean_score_list.append('is not good at')
            else:
                mean_score_list.append('is not evaluated')
        conclude_info = 'To conclude:\n'
        for i in range (10):
            conclude_info += f'\nThe model {mean_score_list[i]} in {field_list[i]} field.\n'
        print(get_score_info)
        print(conclude_info)
        return(get_score_info,conclude_info,plotinfo)

    def report(self,plotinfo,log_path,llm_name,llm_intro):#TODO:用图像展示以下测评结果：各领域题目回答准确率，各领域题目占比，测试题目总数，测试用时等
        """
        log_path:The path of the dialog_init.log
        logger_path:A gloabal variable, the path to the analyse.log

        """
        field = plotinfo[0]
        score_get = plotinfo[1]
        total_score = plotinfo[2]
        totalnum = sum(total_score)

        field_dict = {'knowledge_understanding':'语言理解', 'coding':'代码', 'common_knowledge':'知识与常识', 'reasoning':'逻辑推理', 'multi_language':'多语言', 'specialized_knowledge':'专业知识', 'traceability':'可追溯性', 'outputformatting':'输出格式化', 'internal_security':'内生安全性', 'external_security':'外生安全性'}

        plt.rcParams['font.size'] = 18

        pdf_name = "report.pdf"
        pdf_file_path = os.path.join(logger_path,pdf_name)

        pdf_pages = PdfPages(pdf_file_path)
        # colors = ['blue', 'green', 'red', 'purple', 'orange', 'brown', 'pink', 'gray', 'cyan', 'magenta']

        filtered_fields = [fields for fields, total_scores in zip(field,total_score) if total_scores > 0]
    
        filtered_totalscore = [totalscores for totalscores in total_score if totalscores > 0]
        filtered_score_get = [score for score,total_scores in zip(score_get,total_score) if total_scores > 0]

        #1.背景介绍
        fig = plt.figure(figsize=(30, 30))
        plt.rcParams['font.sans-serif'] = ['SimSun'] 
        plt.rcParams['mathtext.fontset'] = 'stix'

        title = "1.背景介绍"
        plt.title(title, fontsize=32, ha='center',y=1.1, fontfamily='SimSun')

        intro = self.introduction_of_llm(llm_name,log_path,llm_intro)
        # intro = textwrap.fill(intro, width=80)

        fig.text(0.1,0.55, intro, fontsize=25, fontfamily='SimSun',ha='left', va='center')
        plt.axis('off')

        try:
            pdf_pages.savefig(fig)
        except Exception as e:
                warning_message = f"Warning: An report exception occurred - {e}"
                warnings.warn(warning_message, RuntimeWarning)

         #2.测试用例数据信息

        fig, axs = plt.subplots(1, 2, figsize=(30, 30), gridspec_kw={'wspace': 0.15})

        field_info = ''
        if len(filtered_fields)<=3:
            for fields in filtered_fields:
                field_info += f'"{field_dict[str(fields)]}"'
        else:
            for i in range (3):
                field_info += f'"{field_dict[str(filtered_fields[i])]}"'
            field_info += '等领域。'

        testcasenum_info = ''
        for i in range (len(filtered_fields)):
            testcasenum_info += f'\n "{field_dict[filtered_fields[i]]}"领域中有{filtered_totalscore[i]}条测试用例。\n'
        score_info = ''
        for i in range (len(filtered_score_get)):
            score_info += f'\n在"{field_dict[filtered_fields[i]]}"领域中 ,该大语言模型的得分为: {filtered_score_get[i]}/{filtered_totalscore[i]}。\n'

        conclude_info = f'本次测试包括{totalnum}条测试用例.\n\n这些测试用例主要包括' + field_info + f'\n\n在所有测试用例中:\n' + testcasenum_info + score_info
        
        axs[0].text(0,0.55, conclude_info, fontsize=25, ha='left', va='center', fontfamily='SimSun')

        axs[0].axis('off')

        rcParams['font.family'] = 'SimSun'

        #饼状图绘制

        for i in range (len(filtered_fields)):
            filtered_fields[i] = field_dict[filtered_fields[i]]

        for i in range (len(field)):
            field[i] = field_dict[field[i]]

        percentages = [num / totalnum for num in filtered_totalscore]
        patches, texts, autotexts = axs[1].pie(percentages, labels=filtered_fields, autopct='%1.1f%%', startangle=140)
        for autotext in autotexts:
            autotext.set_size(28) 
        for text in texts:
            text.set_size(28)

        axs[1].axis('equal')
        # for i, label in enumerate(field):
        #     plt.text(2, -1 - i * 0.5, label, color=colors[i])
        axs[1] = plt.gca()
        axs[1].set_aspect('equal')  
        axs[1].set_position([0.0, 1.0, 0.6, 0.6])  

        legend_labels = ['{}'.format(filtered_field) for filtered_field in filtered_fields]
        legend = axs[1].legend(patches, legend_labels, loc="lower right", bbox_to_anchor=(1.25, 0.2))

        for label in legend.get_texts():
            label.set_fontsize(30) 
        
        
        axs[1].set_position([0.0, 1.0, 0.6, 0.6])

        axs[1].axis('off')

        plt.subplots_adjust(wspace=0.45)

        title = "2.测试用例数据"
        plt.suptitle(title, fontsize=32, ha='center',y=0.95, fontfamily='SimSun')

        try:
            pdf_pages.savefig(fig)
        except Exception as e:
                warning_message = f"Warning: An report exception occurred - {e}"
                warnings.warn(warning_message, RuntimeWarning)

        #3.错误的测试用例

        fig = plt.figure(figsize=(30, 30))

        title = "3.回答错误的测试用例"
        plt.rcParams['font.sans-serif'] = ['SimSun'] 
        plt.rcParams['mathtext.fontset'] = 'stix'
        plt.title(title, fontsize=32, ha='center',y=1.1, fontfamily='SimSun')

        mistaken_list = extract_mistaken_info(log_path)
        mistaken_txt = ''

        
        for i in range (len(mistaken_list)):
            mistaken_list[i][0] = textwrap.fill(mistaken_list[i][0], width=68)
            mistaken_list[i][1] = textwrap.fill(mistaken_list[i][1], width=68)

        if len(mistaken_list) <= 4:
            for mistakens in mistaken_list:
                if len(mistakens) == 5:
                    if mistakens[2] in field_dict:
                        mistaken = f'\n\n对于以下这条属于"{field_dict[mistakens[2]]}"领域的问题，该大语言模型的回答出现了错误。\n\n问题：“{mistakens[0]}”\n\n回答：“{mistakens[1]}”\n\n该问题的正确答案应包含关键字：{mistakens[3]},不应包含黑名单：{mistakens[4]}。\n\n\n'
                    else:
                        mistaken = f'\n\n对于以下这条属于"{field_dict[mistakens[2]]}"领域的问题，该大语言模型的回答出现了错误。\n\n问题：“{mistakens[0]}”\n\n回答：“{mistakens[1]}”\n\n该问题的正确答案应包含关键字：{mistakens[3]},不应包含黑名单：{mistakens[4]}。\n\n\n'
                    mistaken_txt += mistaken
                else:
                    if mistakens[2] in field_dict:
                        mistaken = f'\n\n对于以下这条属于"{field_dict[mistakens[2]]}"领域的问题，该大语言模型的回答出现了错误。\n\n问题：“{mistakens[0]}”\n\n回答：“{mistakens[1]}”\n\n该问题的正确答案应包含关键字：{mistakens[3]}。\n\n\n'
                    else:
                        mistaken = f'\n\n对于以下这条属于"{mistakens[2]}"领域的问题，该大语言模型的回答出现了错误。\n\n问题：“{mistakens[0]}”\n\n回答：“{mistakens[1]}”\n\n该问题的正确答案应包含关键字：{mistakens[3]}。\n\n\n'
                    mistaken_txt += mistaken
        else:  
            for i in range (4):
                if len(mistaken_list[i]) == 5:
                    if mistaken_list[i][2] in field_dict:
                        mistaken = f'\n\n对于以下这条属于"{field_dict[mistaken_list[i][2]]}"领域的问题，该大语言模型的回答出现了错误。\n\n问题：“{mistaken_list[i][0]}”\n\n回答：“{mistaken_list[i][1]}”\n\n该问题的正确答案应包含关键字：{mistaken_list[i][3]},不应包含黑名单：{mistaken_list[i][4]}。\n\n\n'
                    else:
                        mistaken = f'\n\n对于以下这条属于"{mistaken_list[i][2]}"领域的问题，该大语言模型的回答出现了错误。\n\n问题：“{mistaken_list[i][0]}”\n\n回答：“{mistaken_list[i][1]}”\n\n该问题的正确答案应包含关键字：{mistaken_list[i][3]},不应包含黑名单：{mistaken_list[i][4]}。\n\n\n'
                    mistaken_txt += mistaken
                else:
                    if mistaken_list[i][2] in field_dict:
                        mistaken = f'\n\n对于以下这条属于"{field_dict[mistaken_list[i][2]]}"领域的问题，该大语言模型的回答出现了错误。\n\n问题：“{mistaken_list[i][0]}”\n\n回答：“{mistaken_list[i][1]}”\n\n该问题的正确答案应包含关键字：{mistaken_list[i][3]}。\n\n\n'
                    else:
                        mistaken = f'\n\n对于以下这条属于"{mistaken_list[i][2]}"领域的问题，该大语言模型的回答出现了错误。\n\n问题：“{mistaken_list[i][0]}”\n\n回答：“{mistaken_list[i][1]}”\n\n该问题的正确答案应包含关键字：{mistaken_list[i][3]}。\n\n\n'
                    mistaken_txt += mistaken
        if mistaken_txt == '':
            mistaken_txt += '该LLM完全通过了本次测试，正确回答了所有的测试用例，无错误用例。'

        fig.text(0.1,0.55, mistaken_txt, fontsize=25, fontfamily='SimSun',ha='left', va='center')

        plt.axis('off')

        try:
            pdf_pages.savefig(fig)
        except Exception as e:
                warning_message = f"Warning: An report exception occurred - {e}"
                warnings.warn(warning_message, RuntimeWarning)


        


        #4.各领域测试用例占比的饼图
        # rcParams['font.family'] = 'SimSun'

        # percentages = [num / totalnum for num in filtered_totalscore]
        # plt.figure(figsize=(30, 30))
        # patches, texts, autotexts = plt.pie(percentages, labels=filtered_fields, autopct='%1.1f%%', startangle=140)
        # for autotext in autotexts:
        #     autotext.set_size(28) 
        # for text in texts:
        #     text.set_size(28)

        # plt.title("4.各领域测试用例占比",fontsize=32, y=1.15, fontfamily='SimSun')
        # plt.axis('equal')
        # # for i, label in enumerate(field):
        # #     plt.text(2, -1 - i * 0.5, label, color=colors[i])
        # ax = plt.gca()
        # ax.set_aspect('equal')  
        # ax.set_position([0.2, 0.2, 0.6, 0.6])  

        # legend_labels = ['{}'.format(filtered_field) for filtered_field in filtered_fields]
        # legend = plt.legend(patches, legend_labels, loc="lower left", bbox_to_anchor=(-0.3, -0.3))
        # for label in legend.get_texts():
        #     label.set_fontsize(30) 

        # pdf_pages.savefig()
        # plt.clf()
        
        #5.测试的各领域的得分率柱状图

        accuracies = []
        labels = []
        
        for score, total in zip(score_get, total_score):
            if total == 0:
                # 跳过未测试的数据
                continue
            else:
                accuracy = (score / total) * 100
                label = f"{accuracy:.2f}%"
            accuracies.append(accuracy)
            labels.append(label)

        plt.figure(figsize=(30, 30))                                       
        bars = plt.bar(filtered_fields, accuracies)
        plt.xlabel('领域', fontsize=25, fontfamily='SimSun')
        plt.ylabel('得分率', fontsize=25, fontfamily='SimSun')
        plt.title('4.各领域答题得分率', fontsize=32, y=1.15, fontfamily='SimSun')
        plt.xticks(rotation=45, ha="right", fontsize=28, fontfamily='SimSun')

        for i, (bar, label) in enumerate(zip(bars, labels)):
            plt.text(i, bar.get_height(), label, ha="center", va="bottom", fontsize=28)

        plt.tight_layout()
        pdf_pages.savefig()
        pdf_pages.close()
        print("Report Generated !")

    def introduction_of_llm(self,llm_name,log_path,llm_intro):
        field_dict = {'knowledge_understanding':'语言理解', 'coding':'代码', 'common_knowledge':'知识与常识', 'reasoning':'逻辑推理', 'multi_language':'多语言', 'specialized_knowledge':'专业知识', 'traceability':'可追溯性', 'outputformatting':'输出格式化', 'internal_security':'内生安全性', 'external_security':'外生安全性'}
        name = llm_name
        ex_list = extract_example_info(log_path)
        
        for i in range (len(ex_list)):
            ex_list[i][0] = textwrap.fill(ex_list[i][0], width=70)
            ex_list[i][1] = textwrap.fill(ex_list[i][1], width=70)
        
        example_txt = '以下是本次测试中的几条回答正确的测试用例：\n\n'

        if len(ex_list) == 0:
            example_txt += '本次测试中，该大语言模型未答对任何问题'

        if len(ex_list) <= 3 and len(ex_list) > 0:
            for ex in ex_list:
                example = f'\n\n对于以下这条属于"{field_dict[ex[2]]}"领域的问题，该大语言模型的回答完全正确。\n\n问题：“{ex[0]}”\n\n回答：“{ex[1]}”\n\n'
                example_txt += example
        if len(ex_list) > 3:  
            for i in range (3):
                example = f'\n\n对于以下这条属于"{field_dict[ex_list[i][2]]}"领域的问题，该大语言模型的回答完全正确。\n\n问题：“{ex_list[i][0]}”\n\n回答：“{ex_list[i][1]}”\n\n'
                example_txt += example
        
        intro = '这是一个对于场景化大语言模型的自动化测评报告。\n\n由于工具中暂无关于当前大语言模型的背景信息，所以当前页仅展示本次测评中大语言模型答对的数条测试样例。'

        # if name == 'chatglm_pro':
        #     intro = 'ChatGLMpro 是一款基于人工智能的聊天机器人，它基于清华大学 KEG 实验室与智谱 AI 于 2023 年联合训练的语言模型 GLM 开发而成。\n\nChatGLMpro 具有强大的自然语言处理能力和丰富的知识库，能够理解和回应各种类型的问题和指令，包括但不限于文本生成、问答、闲聊、翻译、推荐等领域。\n\n相比于其他聊天机器人，ChatGLMpro 具有以下优势：\n\n1.高性能的语言模型：ChatGLMpro 基于 GLM 模型，拥有超过 1300 亿参数，能够高效地处理和生成自然语言文本。\n\n2.丰富的知识库：ChatGLMpro 拥有涵盖多个领域的知识库，包括科技、历史、文化、娱乐等方面，能够回应各种类型的问题。\n\n3.强大的问答能力：ChatGLMpro 具有出色的问答能力，能够理解用户的问题并给出准确的回答。\n\n4.个性化交互：ChatGLMpro 能够根据用户的语气和兴趣进行个性化交互，让用户感受到更加自然的对话体验。\n\n5.开放的接口：ChatGLMpro 还提供了开放的接口，方便其他应用程序和企业将其集成到自己的系统中。\n\n总的来说，ChatGLMpro 是一款高性能、智能化、多功能的聊天机器人，能够为企业和个人提供高效的智能化服务。\n\n本次对该大语言模型的测试涉及多个领域的问题，测试的结果和分析如下文所示。\n\n'
        #     intro += example_txt
        #     return intro
        # if name == 'qwen_turbo':
        #     intro = '通义千问是由阿里巴巴集团开发的一款人工智能语言模型应用，它采用了大规模机器学习技术，能够模拟人类自然语言的能力，提供多种服务，如文本翻译、聊天机器人、\n\n自动回复、文档摘要等。\n\n它的核心特点是多轮对话，可以理解用户的意图并进行有效的回复；同时，它还具有强大的文案创作能力，可以为用户提供优秀的文字创意，比如续写小说、撰写邮件等。\n\n此外，通义千问还具备多模态的知识理解能力，可以识别图片、音频、视频等多种媒体形式，并从中提取出关键信息。不仅如此，通义千问还支持多语言，可以实现中文、\n\n英文等不同语言之间的自由转换。\n\n目前，通义千问正在接受内测阶段，并已在各大手机应用市场上线，所有人都可以通过APP直接体验最新模型能力。\n\n本次对该大语言模型的测试涉及多个领域的问题，测试的结果和分析如下文所示。\n\n'
        #     intro += example_txt
        #     return intro
        # if name == 'wenxin':
        #     intro = '背景介绍：百度是一家全球领先的人工智能公司，拥有强大的技术实力和丰富的数据资源。近年来，百度在自然语言处理领域取得了重大突破，其中最具代表性的就是文心一言。技术原理：文心一言是基于深度学习算法和大规模语料库训练得到的。它采用了Transformer架构，这是一种基于自注意力机制的神经网络结构。通过多轮训练和优化，文心一言可以学会从海量文本中提取语义信息，并根据上下文生成合理的回复。\n\n功能特点：\n\n（1）对话互动：文心一言能够与用户进行自然对话，理解并回答用户的问题，提供相关的知识和信息。\n\n（2）回答问题：文心一言可以针对用户提出的问题进行快速回答，无需等待人工响应。\n\n（3）协助创作：文心一言能够根据用户的创作需求，提供灵感和素材，帮助用户更好地完成写作任务。\n\n（4）多语言支持：文心一言支持多种语言，可以为不同语言的用户提供服务。\n\n（5）知识推理：文心一言具备进行知识推理的能力，可以根据已有的知识进行推理，为用户提供更为精准的信息。\n\n应用场景：\n\n（1）搜索引擎：百度将文心一言应用于搜索引擎中，为用户提供更为准确和及时的搜索结果。\n\n（2）智能客服：文心一言可以应用于企业客服系统中，提高客户服务效率和质量。\n\n（3）智能家居：文心一言可以与智能家居设备结合，为用户提供更为智能化的家居生活体验。\n\n（4）教育领域：文心一言可以为教育领域提供支持，辅助教师进行教学和学生进行自主学习。\n\n（5）其他领域：文心一言还可以应用于新闻媒体、广告营销、金融投资等领域，提高工作效率和服务质量。\n\n未来发展：\n\n随着技术的不断进步和应用场景的不断扩展，文心一言将会拥有更加广泛的应用前景。百度将继续投入大量资源和精力，对文心一言进行持续优化和升级，提高其性能和智能化\n\n程度，为用户提供更为优质的服务。同时，百度也将加强与各行业企业的合作，推动人工智能技术的普及和应用，促进社会进步和发展。\n\n本次对该大语言模型的测试涉及多个领域的问题，测试的结果和分析如下文所示。\n\n'
        #     intro += example_txt
        #     return intro
        if llm_intro != '':
            llm_intro = '\n\n'.join([textwrap.fill(paragraph, width=76) for paragraph in llm_intro.split('\n\n')])
            intro = llm_intro
            intro += '\n\n本次对该大语言模型的测试涉及多个领域的问题，测试的结果和分析如下文所示。\n\n'
            intro += example_txt
        return intro









        
