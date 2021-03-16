import React, {Component} from 'react';

import '../stylesheets/App.css';
import Question from './Question';
import Search from './Search';
import $ from 'jquery';

class QuestionView extends Component {
  constructor() {
    super();
    this.state = {
      questions: [],
      page: 1,
      totalQuestions: 0,
      categories: {},
      currentCategory: null,
      currentSearch: null,
    }
  }

  componentDidMount() {
    this.getQuestions();
  }

  getQuestions = () => {
    $.ajax({
      url: `api/questions?page=${this.state.page}`,
      type: "GET",
      success: (result) => {
        this.setState({
          questions: result.questions,
          totalQuestions: result.total_questions,
          categories: result.categories,
          currentCategory: null,
          currentSearch: null
        })
        return;
      },
      error: (error) => {
        alert('Unable to load questions. Please try your request again')
        return;
      }
    })
  }

  getByCategory = (id) => {
    $.ajax({
      url: `/api/categories/${id}/questions?page=${this.state.page}`,
      type: "GET",
      success: (result) => {
        this.setState({
          questions: result.questions,
          totalQuestions: result.total_questions,
          currentCategory: result.current_category,
          currentSearch: null
        })
        return;
      },
      error: (error) => {
        alert('Unable to load questions. Please try your request again')
        return;
      }
    })
  }


  submitSearch = (searchTerm) => {
    $.ajax({
      url: `/api/questions/search?page=${this.state.page}`,
      type: "POST",
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({searchTerm: searchTerm, categoryId: this.state.currentCategory}),
      xhrFields: {
        withCredentials: true
      },
      crossDomain: true,
      success: (result) => {
        this.setState({
          questions: result.questions,
          totalQuestions: result.total_questions,
          currentSearch: searchTerm,
        })
        return;
      },
      error: (error) => {
        alert('Unable to load questions. Please try your request again')
        return;
      }
    })
  }

  selectPage(num) {
    this.setState({page: num}, () => {
      if (this.state.currentSearch) {
        // Continue in active questions by search view
        this.submitSearch(this.state.currentSearch);
      } else if (this.state.currentCategory) {
        // Continue in active questions by category view
        this.getByCategory(this.state.currentCategory);
      } else {
        // Continue in active questions by list view
        this.getQuestions();
      }
    });
  }

  createPagination() {
    console.log('here');
    let pageNumbers = [];
    const items_per_page = 10
    let maxPage = Math.ceil(this.state.totalQuestions / items_per_page)
    for (let i = 1; i <= maxPage; i++) {
      pageNumbers.push(
          <span
              key={i}
              className={`page-num ${i === this.state.page ? 'active' : ''}`}
              onClick={() => {
                this.selectPage(i)
              }}>{i}
        </span>)
    }
    return pageNumbers;
  }

  questionAction = (id) => (action) => {
    if (action === 'DELETE') {
      if (window.confirm('are you sure you want to delete the question?')) {
        $.ajax({
          url: `/api/questions/${id}`,
          type: "DELETE",
          success: (result) => {
            this.getQuestions();
          },
          error: (err) => {
            let status_code = err.status ? err.status  : 500;
            let msg = 'There was an unexpected error while trying to delete the Question (500)'
            if (status_code === 404) {
                msg = 'Could not find Question to delete (404)';
            }
            alert(msg)
            return;
          }
        })
      }
    }
  }

  render() {
    return (
        <div className="question-view">
          <div className="categories-list">
            <h2 onClick={() => {
              this.getQuestions()
            }}>Categories</h2>
            <ul>
              {Object.keys(this.state.categories).map((id,) => (
                  <li key={id} onClick={() => {
                    this.getByCategory(id)
                  }}>
                    {this.state.categories[id]}
                    <img className="category" src={`${this.state.categories[id]}.svg`}/>
                  </li>
              ))}
            </ul>
            <Search submitSearch={this.submitSearch}/>
          </div>
          <div className="questions-list">
            <h2>Questions</h2>
            {this.state.questions.map((q, ind) => (
                <Question
                    key={q.id}
                    question={q.question}
                    answer={q.answer}
                    category={this.state.categories[q.category]}
                    difficulty={q.difficulty}
                    questionAction={this.questionAction(q.id)}
                />
            ))}
            <div className="pagination-menu">
              {this.createPagination()}
            </div>
          </div>

        </div>
    );
  }
}

export default QuestionView;
