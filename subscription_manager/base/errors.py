"""
Copyright 2019 EUROCONTROL
==========================================

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the 
following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following 
   disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following 
   disclaimer in the documentation and/or other materials provided with the distribution.
3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products 
   derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, 
INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, 
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, 
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE 
USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

==========================================

Editorial note: this license is an instance of the BSD license template as provided by the Open Source Initiative: 
http://opensource.org/licenses/BSD-3-Clause

Details on EUROCONTROL: http://www.eurocontrol.int
"""
import typing as t
from http import HTTPStatus

from flask import request
from werkzeug.exceptions import HTTPException

__author__ = "EUROCONTROL (SWIM)"


class APIError(Exception):
    title = None
    detail = None
    status = HTTPStatus.BAD_REQUEST

    def __init__(self, detail, status=None):
        self.detail = detail

        if status is not None:
            self.status = status


class BadRequestError(APIError):
    title = 'Bad Request'
    status = HTTPStatus.BAD_REQUEST


class NotFoundError(APIError):
    title = 'Not Found'
    status = HTTPStatus.NOT_FOUND


class UnauthorizedError(APIError):
    title = 'Unauthorized'
    status = HTTPStatus.UNAUTHORIZED


class ForbiddenError(APIError):
    title = 'Forbidden'
    status = HTTPStatus.FORBIDDEN


class ConflictError(APIError):
    title = 'Conflict'
    status = HTTPStatus.CONFLICT


def process_error(error: t.Union[HTTPException, APIError, t.Any]) -> t.Dict[str, str]:
    """
    :param error: The error raised from the request
    :return: The response body of the error
    """
    if isinstance(error, HTTPException):
        status = error.code
        title = error.name
        detail = error.description
    elif isinstance(error, APIError):
        status = error.status.value
        title = error.title
        detail = error.detail
    else:
        raise error
        status = HTTPStatus.INTERNAL_SERVER_ERROR.value
        title = 'Internal Server Error'
        detail = 'The server has encountered an error during the request'

    body = {
        "status": status,
        "title": title,
        "detail": detail
    }

    return body
