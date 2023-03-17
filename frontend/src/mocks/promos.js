export const def = {
    "openapi": "3.0.2",
    "info": {
        "title": "promo",
        "version": "0.1.0"
    },
    "paths": {
        "/api/v1/promo/code/{code}": {
            "get": {
                "summary": "Get By Code",
                "description": "Получить информацию о промокоде по уникальному коду",
                "operationId": "get_by_code_api_v1_promo_code__code__get",
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "title": "Code",
                            "type": "string"
                        },
                        "name": "code",
                        "in": "path"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/Promo"
                                }
                            }
                        }
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        }
                    }
                }
            }
        },
        "/api/v1/promo/user/{user_id}": {
            "get": {
                "summary": "Get By User Id",
                "description": "Получить информацию о промокодах для пользователя",
                "operationId": "get_by_user_id_api_v1_promo_user__user_id__get",
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "title": "User Id",
                            "type": "string",
                            "format": "uuid"
                        },
                        "name": "user_id",
                        "in": "path"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "title": "Response Get By User Id Api V1 Promo User  User Id  Get",
                                    "type": "array",
                                    "items": {
                                        "$ref": "#/components/schemas/Promo"
                                    }
                                }
                            }
                        }
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        }
                    }
                }
            }
        },
        "/api/v1/promo/activate": {
            "post": {
                "summary": "Activate",
                "description": "Активировать промокод",
                "operationId": "activate_api_v1_promo_activate_post",
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "title": "Code",
                            "type": "string"
                        },
                        "name": "code",
                        "in": "query"
                    },
                    {
                        "required": true,
                        "schema": {
                            "title": "User Id",
                            "type": "string",
                            "format": "uuid"
                        },
                        "name": "user_id",
                        "in": "query"
                    },
                    {
                        "required": true,
                        "schema": {
                            "title": "Service Id",
                            "type": "string",
                            "format": "uuid"
                        },
                        "name": "service_id",
                        "in": "query"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/ActivationResult"
                                }
                            }
                        }
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        }
                    }
                }
            }
        },
        "/api/v1/promo/deactivate": {
            "post": {
                "summary": "Deactivate",
                "description": "Деактивировать промокод",
                "operationId": "deactivate_api_v1_promo_deactivate_post",
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "title": "Code",
                            "type": "string"
                        },
                        "name": "code",
                        "in": "query"
                    },
                    {
                        "required": true,
                        "schema": {
                            "title": "User Id",
                            "type": "string",
                            "format": "uuid"
                        },
                        "name": "user_id",
                        "in": "query"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/DeactivationResult"
                                }
                            }
                        }
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        }
                    }
                }
            }
        }
    },
    "components": {
        "schemas": {
            "ActivationResult": {
                "title": "ActivationResult",
                "required": [
                    "result"
                ],
                "type": "object",
                "properties": {
                    "result": {
                        "title": "Result",
                        "type": "boolean"
                    },
                    "discount_type": {
                        "$ref": "#/components/schemas/DiscountType"
                    },
                    "discount_amount": {
                        "title": "Discount Amount",
                        "type": "number"
                    },
                    "error_message": {
                        "title": "Error Message",
                        "type": "string"
                    }
                }
            },
            "DeactivationResult": {
                "title": "DeactivationResult",
                "required": [
                    "result"
                ],
                "type": "object",
                "properties": {
                    "result": {
                        "title": "Result",
                        "type": "boolean"
                    },
                    "error_message": {
                        "title": "Error Message",
                        "type": "string"
                    }
                }
            },
            "DiscountType": {
                "title": "DiscountType",
                "enum": [
                    "PRICE_FIX",
                    "DISCOUNT_PERCENT",
                    "DISCOUNT_FIX"
                ],
                "type": "string",
                "description": "An enumeration."
            },
            "HTTPValidationError": {
                "title": "HTTPValidationError",
                "type": "object",
                "properties": {
                    "detail": {
                        "title": "Detail",
                        "type": "array",
                        "items": {
                            "$ref": "#/components/schemas/ValidationError"
                        }
                    }
                }
            },
            "Promo": {
                "title": "Promo",
                "required": [
                    "id",
                    "title",
                    "description",
                    "code",
                    "start_at",
                    "expired",
                    "user_id",
                    "all_activations_count",
                    "left_activations_count",
                    "discount_type",
                    "discount_amount",
                    "service_ids"
                ],
                "type": "object",
                "properties": {
                    "id": {
                        "title": "Id",
                        "type": "string",
                        "format": "uuid"
                    },
                    "title": {
                        "title": "Title",
                        "type": "string"
                    },
                    "description": {
                        "title": "Description",
                        "type": "string"
                    },
                    "code": {
                        "title": "Code",
                        "type": "string"
                    },
                    "start_at": {
                        "title": "Start At",
                        "type": "string",
                        "format": "date-time"
                    },
                    "expired": {
                        "title": "Expired",
                        "type": "string",
                        "format": "date-time"
                    },
                    "user_id": {
                        "title": "User Id",
                        "type": "string",
                        "format": "uuid"
                    },
                    "all_activations_count": {
                        "title": "All Activations Count",
                        "type": "integer"
                    },
                    "left_activations_count": {
                        "title": "Left Activations Count",
                        "type": "integer"
                    },
                    "discount_type": {
                        "$ref": "#/components/schemas/DiscountType"
                    },
                    "discount_amount": {
                        "title": "Discount Amount",
                        "type": "number"
                    },
                    "service_ids": {
                        "title": "Service Ids",
                        "type": "array",
                        "items": {
                            "type": "string",
                            "format": "uuid"
                        }
                    }
                }
            },
            "ValidationError": {
                "title": "ValidationError",
                "required": [
                    "loc",
                    "msg",
                    "type"
                ],
                "type": "object",
                "properties": {
                    "loc": {
                        "title": "Location",
                        "type": "array",
                        "items": {
                            "type": "string"
                        }
                    },
                    "msg": {
                        "title": "Message",
                        "type": "string"
                    },
                    "type": {
                        "title": "Error Type",
                        "type": "string"
                    }
                }
            }
        }
    }
}