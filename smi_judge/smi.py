from rdkit import Chem
from rdkit.Chem import Draw

from typing import TypedDict, Annotated, Any
from langgraph.graph.message import add_messages
from langchain_core.messages import AIMessage
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver


import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com")

def guess_info_from_wrong_smi(text: str) -> str | None:
    """
    用 LLM 从自然语言描述中猜一个 SMILES。
    猜不到就返回 None。
    """
    prompt = f"""
你是一个有机化学助手。用户会用自然语言描述一个常见分子。
你的任务是：尝试从一个错误的SMILES中猜出这个SMILES代表的分子。

要求：
- 输出这个分子是什么
- 给出这个 SMILES 错误的理由
- 尽量简洁

用户描述：
{text}
""".strip()

    resp = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.choices[0].message.content

def judge_smi (smi):
    """若 smi 合法，则返回原始 smi，否则返回 None"""
    mol = Chem.MolFromSmiles(smi)
    return smi if mol is not None else None

def smi_to_graph(smi):

    mol = Chem.MolFromSmiles(smi)
    graph = Draw.MolToImage(mol)
    return graph

class SearchState(TypedDict):
    messages: Annotated[list, add_messages]
    user_query: str      # 用户原始输入
    smi: str | None      # judge 后得到的 smi（合法）或 None（不合法）
    mol_image: Any | None  # 画出来的图像对象（PIL.Image）
    step: str            # 标记当前步骤

def search_smi(state: SearchState) -> dict:
    """步骤2：judge 节点：验证 SMILES 合法性"""
    user_query = state["user_query"]
    print(f"🔍 正在验证: {user_query}")
    smi = judge_smi(user_query)

    if smi is None:
        # 非法 SMILES，交给下一个节点用 LLM 猜
        return {
            "smi": None,
            "step": "judge_failed",
            "messages": [AIMessage(content="❌ 这不是合法的 SMILES，我会尝试让下一个节点用 LLM 猜。")]
        }
    else:
        # 合法 SMILES，直接传给 draw 节点
        return {
            "smi": smi,
            "step": "judge_ok",
            "messages": [AIMessage(content="✅ 这是合法的 SMILES，将为你生成分子图。")]
        }

def draw(state: SearchState) -> dict:
    """draw 节点：根据 smi 画分子图，或做 fallback"""
    smi = state.get("smi")
    step = state.get("step")
    user_text = state.get("user_query", "")

  # 情况 2：没有合法 SMILES，可以在这里实现 “LLM 猜 SMILES”
    if smi is None:
        explanation = guess_info_from_wrong_smi(user_text)
        return {
            "mol_image": None,
            "step": "draw_from_error",
            "messages": [AIMessage(content=explanation)]
        }

    # 情况 3：正常路径，有合法 SMILES，画图
    mol_image = smi_to_graph(smi)

    return {
        "mol_image": mol_image,
        "step": "draw_ok",
        "messages": [AIMessage(content="🧪 分子图已生成。")]
    }


def create_search_assistant():
    workflow = StateGraph(SearchState)
    
    # 添加节点
    workflow.add_node("judge", search_smi)
    workflow.add_node("draw", draw)
    
    # 设置线性流程
    workflow.add_edge(START, "judge")
    workflow.add_edge("judge", "draw")
    workflow.add_edge("draw", END)
    
    # 编译图
    app = workflow.compile()
    return app


if __name__ == "__main__":
    app = create_search_assistant()

    # 例 1：合法 SMILES
    print("\n===== 测试合法 SMILES =====")
    init_state_ok = {
        "user_query": "CCO",
        "messages": [],
        "smi": None,
        "mol_image": None,
        "step": "start",
    }
    result_ok = app.invoke(init_state_ok)
    print("step:", result_ok["step"])
    print("LLM 消息:", result_ok["messages"][-1].content)

    img1 = result_ok["mol_image"]
    if img1:
        img1.save("mol_ok.png")
        print("保存图片：mol_ok.png")

    # 例 2：错误 SMILES
    print("\n===== 测试错误 SMILES =====")
    init_state_bad = {
        "user_query": "C1=CC=CC=C",   # 少一个闭环
        "messages": [],
        "smi": None,
        "mol_image": None,
        "step": "start",
    }
    result_bad = app.invoke(init_state_bad)
    print("step:", result_bad["step"])
    print("LLM 消息:", result_bad["messages"][-1].content)
