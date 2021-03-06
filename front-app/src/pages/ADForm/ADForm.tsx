import React, { memo } from "react";
import styled from "styled-components";
import { QuestionList } from "./components/QuestionList";
import { useADForm } from "./useADForm";
import { Form } from "./components/Form";
import { Button } from "@material-ui/core";

const MainContainer = styled.div`
  height: 550px;
  display: flex;
  flex: 1;
  flex-direction: row;
  margin-top: 50px;
  margin-bottom: 50px;
  background-color: white;
`;

const QuestionListContainer = styled.div`
  flex: 1;
  align-items: center;
  margin-right: 15px;
  padding-right: 10px;
  padding-left: 10px;
`;

const ListTitle = styled.h3`
  text-align: center;
  padding-bottom: 10px;
  border-bottom: 2px solid;
`;

const Divider = styled.div`
  width: 0.5px;
  height: 450px;
  align-self: center;
  background-color: black;
`;

const FormContainer = styled.div`
  flex: 3;
  display: flex;
  flex-direction: column;
  padding-right: 10px;
  margin-left: 15px;
  padding-left: 10px;
  padding-bottom: 10px;
`;

const DirectionButtonsContainer = styled.div`
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  padding: 30px;
`;

const ADFormComponent = () => {
  const {
    formik,
    questions,
    currentQuestionIndex,
    goToPreviousQuestion,
    goToNextQuestion,
  } = useADForm();

  if (questions.length === 0) {
    return (
      <MainContainer>
        <p>Une erreur est survenue</p>
      </MainContainer>
    );
  }

  return (
    <MainContainer>
      <QuestionListContainer>
        <ListTitle>Questions</ListTitle>
        <QuestionList
          questions={questions}
          answers={formik.values}
          currentQuestionIndex={currentQuestionIndex}
          // errors={formik.errors} TBD WHEN WE'LL MANAGE ERRORS
        />
      </QuestionListContainer>
      <FormContainer>
        <Form question={questions[currentQuestionIndex]} formik={formik} />
        <DirectionButtonsContainer>
          <Button
            variant="contained"
            onClick={goToPreviousQuestion}
            disabled={currentQuestionIndex === 0}
          >
            Précédent
          </Button>
          {currentQuestionIndex < questions.length - 1 ? (
            <Button variant="contained" onClick={goToNextQuestion}>
              Suivant
            </Button>
          ) : (
            <Button variant="contained" onClick={() => formik.handleSubmit()}>
              Envoyer
            </Button>
          )}
        </DirectionButtonsContainer>
      </FormContainer>
    </MainContainer>
  );
};

export const ADForm = memo(ADFormComponent);
