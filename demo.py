# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time  : 2022/5/21 18:51
# Author: jgw


from pymongo import MongoClient
from fastapi import FastAPI
from pydantic import BaseModel
from bson import ObjectId
import uvicorn

"""
Demo
"""


class User(BaseModel):
	name: str
	age: int
	department: str
	phonenum: str
	address: str


mongo_client = MongoClient('mongodb://root:root@192.168.0.250:27017/?authMechanism=DEFAULT&authSource=admin')
db = mongo_client['info']
cl = db['user_info']

app = FastAPI(title="用户信息管理系统")


@app.post('/user/info/add')
async def add_user(user: User):
	"""
	新增一条用户信息
	:return:
	"""
	cl.insert_one(user.dict())

	return 'SUCCESS: 成功添加1条用户信息'


@app.get('/user/info/list')
async def get_user_list():
	"""
	获取用户信息列表
	:return:
	"""
	add_fields_stage = {"$addFields": {
		'_id': {"$toString": "$_id"}
	}}

	project_stage = {"$project": {
		'age': False,
		'address': False
	}}

	pipeline = [
		add_fields_stage,
		project_stage
	]

	return list(cl.aggregate(pipeline))


@app.get('/user/info/detail/{_id}')
async def get_user_detail(_id: str):
	"""
	获取某用户的详细信息
	:return:
	"""
	return cl.find_one(
		{'_id': ObjectId(_id)},
		{
			'_id': {"$toString": "$_id"},
			'name': True,
			'age': True,
			'phonenum': True,
			'department': True,
			'address': True
		}
	)


@app.put('/user/info/update/{_id}')
async def update_user(_id: str, user: User):
	"""
	修改1条用户信息
	:return:
	"""
	cl.update_one({'_id': ObjectId(_id)}, {"$set": user.dict()})

	return 'SUCCESS: 成功修改1条用户信息'


@app.delete('/user/info/{_id}')
async def delete_user(_id: str):
	"""
	删除1条用户信息
	:param _id: 要删除的用户的主键
	:return:
	"""
	cl.delete_one({'_id': ObjectId(_id)})

	return 'SUCCESS: 成功删除1条用户信息'


if __name__ == '__main__':
	uvicorn.run(app='demo:app', reload=True, debug=True)
	pass
